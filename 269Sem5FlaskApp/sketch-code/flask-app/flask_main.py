from flask import Flask, render_template, request
import requests
from flask_ngrok import run_with_ngrok
import os
import sys
import pdb
import time


args = sys.argv
if (len(args)!=2 or "--path=" not in args[1]):
  raise Exception("Invalid command line please specify path=root folder")
root_folder = args[1][args[1].index("=")+1:]
model_folder = root_folder+"model"
model_json = model_folder+"/model_json.json"
model_weights = model_folder+"/weights.h5"
output_folder = root_folder+"/flask-app/templates"

sys.path.append(os.path.abspath(root_folder+"src"))
from convert_single_image import call_from_api
import json
from pathlib import Path
import shutil

import ruclip
from rudalle.pipelines import generate_images, show, super_resolution, cherry_pick_by_ruclip
from rudalle import get_rudalle_model, get_tokenizer, get_vae, get_realesrgan
from rudalle.utils import seed_everything
import translators


# prepare models:
device = 'cuda'
dalle = get_rudalle_model('Malevich', pretrained=True, fp16=True, device=device)
tokenizer = get_tokenizer()
vae = get_vae(dwt=True).to(device)

# pipeline utils:
realesrgan = get_realesrgan('x2', device=device)
clip, processor = ruclip.load('ruclip-vit-base-patch32-384', device=device)
clip_predictor = ruclip.Predictor(clip, processor, device, bs=8)
seed_everything(42)


app = Flask(__name__)
run_with_ngrok(app)

START_REMOVABLE_CONTENT = "<!--START OF REMOVAL SECTION-->\n"
END_REMOVABLE_CONTENT = "<!--END OF REMOVAL SECTION-->"

dirpath = Path(root_folder+"flask-app/uploaded_images")
if dirpath.exists() and dirpath.is_dir():
  shutil.rmtree(dirpath)
  Path(root_folder+"flask-app/uploaded_images").mkdir(parents=True, exist_ok=True)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload-image",methods=["POST"])
def upload_image():
    files = request.files['file']
    path = os.path.join(root_folder+"flask-app/uploaded_images",files.filename)
    files.save(path)
    call_from_api(path,model_json,model_weights,output_folder)
    return 'OK', 200

@app.route("/sample-image/<name>", methods=["POST"])
def upload_sample_image(name):
    path =root_folder+"flask-app/static/images/"+name+".png"
    call_from_api(path,model_json,model_weights,output_folder)
    return 'OK', 200


@app.route("/upload-feature-image",methods=["POST"])
def upload_feature_image():
    files = request.files['file']
    path = os.path.join(root_folder+"flask-app/uploaded_images",files.filename)
    files.save(path)
    return 'OK', 200

@app.route("/generate-images-for-text",methods=["POST"])
def image_generator():
  text = request.form["image_caption"]
  text = translators.google(text, from_language='en', to_language='ru')
  ele_id = request.form["ele_id"]
  pil_images = []
  scores = []
  for top_k, top_p, images_num in [(1024, 0.995, 8)]:
      _pil_images, _scores = generate_images(text, tokenizer, dalle, vae, top_k=top_k, images_num=images_num, bs=8, top_p=top_p)
      pil_images += _pil_images
      scores += _scores
  top_images, clip_scores = cherry_pick_by_ruclip(pil_images, text, clip_predictor, count=4)
  sr_images = super_resolution(top_images, realesrgan)
  file_string="generated_image"
  for filename in os.listdir(root_folder+"flask-app/static/images"):
        if filename.startswith('generated_image'):  # not to remove other images
            os.remove(root_folder+"flask-app/static/images/"+filename)
  timestamp = str(int(time.time()))
  for i in range(len(sr_images)):
    filename = root_folder+"flask-app/uploaded_images/" + file_string+"_"+str(i+1)+"_"+ele_id+"_"+timestamp+".jpg"
    sr_images[i].resize((150,150)).save(filename)
    filename2 = root_folder+"flask-app/static/images/" + file_string+"_"+str(i+1)+"_"+ele_id+"_"+timestamp+".jpg"
    sr_images[i].resize((150,150)).save(filename2)
  return timestamp


def create_modified_html(orig_content, changes):
  new_content = orig_content
  for change in changes:
    value = changes[change]
    change_type = change[0:change.index("_")]
    if (value=="null" and change_type=="imgpicker"):
      continue
    change_id = change[change.index("_")+1:change.rindex("_")]
    if (change_id in ["sidebar_wrapper","footer_wrapper","navbar_wrapper","header_wrapper","webpage_body","full_wrapper"]):
      change_id = change_id.replace("_","-")
    print (change_type, change_id)

    if (change_type == "fgcolorpicker"):
      element_index = new_content.index("id=\""+change_id+"\"")
      left_side = new_content[0:element_index]
      right_side = new_content[element_index:]
      open_index = left_side.rindex("<")
      close_index = right_side.index(">")
      element_string = new_content[open_index:element_index+close_index+1]
      old_element_string = element_string
      if "style=" in element_string:
        style_index = element_string.index("style=")
        style_end_index = element_string[style_index + 7:].index("\"")
        style_sub_string = element_string[style_index:style_index + 7+style_end_index]
        element_string = element_string.replace(style_sub_string, style_sub_string+" color:"+value+" !important;")
      else:
        element_string = element_string[:-1] + " style=\"color:"+value+" !important;\">"
      new_content = new_content.replace(old_element_string, element_string)

    elif (change_type == "bgcolorpicker"):
      element_index = new_content.index("id=\""+change_id+"\"")
      left_side = new_content[0:element_index]
      right_side = new_content[element_index:]
      open_index = left_side.rindex("<")
      close_index = right_side.index(">")
      element_string = new_content[open_index:element_index+close_index+1]
      old_element_string = element_string
      if "style=" in element_string:
        style_index = element_string.index("style=")
        style_end_index = element_string[style_index + 7:].index("\"")
        style_sub_string = element_string[style_index:style_index + 7+style_end_index]
        element_string = element_string.replace(style_sub_string, style_sub_string+" background-color:"+value+" !important;")
      else:
        element_string = element_string[:-1] + " style=\"background-color:"+value+" !important;\">"
      new_content = new_content.replace(old_element_string, element_string)
    
    elif (change_type == "imgpicker"):
      element_index = new_content.index("id=\""+change_id+"\"")
      left_side = new_content[0:element_index]
      right_side = new_content[element_index:]
      open_index = left_side.rindex("<")
      close_index = right_side.index(">")
      element_string = new_content[open_index:element_index+close_index+1]
      old_element_string = element_string
      if "style=" in element_string:
        style_index = element_string.index("style=")
        style_end_index = element_string[style_index + 7:].index("\"")
        style_sub_string = element_string[style_index:style_index + 7+style_end_index]
        element_string = element_string.replace(style_sub_string, style_sub_string+" background: url(../static/images/"+value+"); background-size: cover; background-position: 50% 50%;")
      else:
        element_string = element_string[:-1] + " style=\"background: url(../static/images/"+value+"); background-size: cover; background-position: 50% 50%;\">"
      new_content = new_content.replace(old_element_string, element_string)
    elif (change_type == "textpicker"):
      element_index = new_content.index("id=\""+change_id+"\"")
      right_side = new_content[element_index:]
      close_index = right_side.index(">")
      start = element_index+close_index+1
      end = start+new_content[start:].index("</")
      new_content = new_content.replace(new_content[start:end],value)
  
  while START_REMOVABLE_CONTENT in new_content:
    start = new_content.index(START_REMOVABLE_CONTENT)
    end = new_content.index(END_REMOVABLE_CONTENT)+len(END_REMOVABLE_CONTENT)
    new_content = new_content[:start] + new_content[end:]

  new_content_list = new_content.split("\n")
  final_content_list = []
  for i in new_content_list:
    if len(i.lstrip())!=0:
      final_content_list.append(i)
  new_content = '\n'.join(final_content_list)
  return new_content

def create_and_save_modified_html(orig_content, changes):
  #Instead of creating a download, first create a folder and zip it. Then try creating a dummy anchor tag with download, sending the zip path as return from request. Then download that zip 
  new_content = create_modified_html(orig_content, changes)

  #Create folder
  parent = root_folder+"flask-app/"
  dirpath = Path(parent+"output")
  if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)
  Path(parent+"output/templates").mkdir(parents=True, exist_ok=True)
  shutil.copytree(parent+"static/css",parent+"output/static/css")
  shutil.copytree(parent+"static/js",parent+"output/static/js")
  shutil.copytree(parent+"uploaded_images",parent+"output/static/images")
  with open(parent+"output/templates/result.html","w") as new_file:
    new_file.write(new_content)
  timestamp = str(int(time.time()))
  shutil.make_archive(parent+"static/SketchResult"+timestamp, 'zip', parent+"output")
  return "../static/SketchResult"+timestamp+".zip"

@app.route("/preview-html-prepare/<name>",methods=["POST"])
def preview_html_prepare(name):
    changes = json.loads(request.form["changes"])
    path = os.path.join(root_folder+"flask-app/templates",name+".html")
    with open(path,"r") as file:
      orig_content = file.read()
    new_content = create_modified_html(orig_content, changes)
    parent = root_folder+"flask-app/"
    with open(parent+"/templates/preview.html","w") as new_file:
      new_file.write(new_content)
    return 'OK', 200

@app.route("/preview-html")
def preview_html():
    return render_template('preview.html')

@app.route("/download-html/<name>",methods=["POST"])
def download_html(name):
    # print(request.form)
    changes = json.loads(request.form["changes"])
    path = os.path.join(root_folder+"flask-app/templates",name+".html")
    with open(path,"r") as file:
      orig_content = file.read()
    zipfile = create_and_save_modified_html(orig_content, changes)
    return zipfile, 200



@app.route("/generated/<name>")
def generated(name):
    return render_template(name+'.html')

@app.route("/generated-image/<name>")
def generated_image(name):
    return root_folder+"flask-app/uploaded-images/"+name+".jpg"

@app.route("/init/")
def initial():
    return render_template('init.html')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run()
