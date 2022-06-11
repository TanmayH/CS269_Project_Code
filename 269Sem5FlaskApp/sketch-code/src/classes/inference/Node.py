from __future__ import print_function
from __future__ import absolute_import

from .SamplerUtils import *

TEXT_PLACE_HOLDER = "[]"
START_REMOVABLE_CONTENT = "<!--START OF REMOVAL SECTION-->\n"
END_REMOVABLE_CONTENT = "<!--END OF REMOVAL SECTION-->\n"

class Node:

    def __init__(self, key, parent_node, content_holder):
        self.key = key
        self.parent = parent_node
        self.children = []
        self.content_holder = content_holder

    def add_child(self, child):
        self.children.append(child)

    def show(self):
        for child in self.children:
            child.show()

    def rendering_function(self, key, value):
      value = value.replace(TEXT_PLACE_HOLDER, SamplerUtils.get_random_text())
      return value
    
    def detailed_rendering_function(self, key, value):
      value = value.replace(TEXT_PLACE_HOLDER, SamplerUtils.get_random_text(360,36,True))
      return value
    
    def nav_class_replacement(self, value):
      pass

    def render(self, mapping, rendering_function=None,spacing=12,script_holder=""):
        content = ""
        nav_style = ""
        nav_title_placeholder = ""
        sidebar_title_placeholder = ""
        carousel_indicators = 0
        layout_type = ""
        child_count = 0
        tab_title = ""
        carousel_title = ""
        collapse_id = ""
        checkbox_id = ""
        
        text_id = ""
        date_id = ""
        range_id = ""
        feature_ele_id = ""
        ol_id = ""
        ul_id = ""
        para_id = ""
        table_id = ""
        textFieldId = ""
        component_id = ""

        id_text = SamplerUtils.get_random_text(8,0)
        if (self.key == "tabs"):
          tab_title = id_text
        elif (self.key == "carousel"):
          carousel_title = "carousel_"+id_text
          component_id = carousel_title
        elif (self.key == "mix-collapse"):
          collapse_id = id_text
        elif (self.key == "row" or self.key=="row-double"):
          checkbox_id = id_text
        elif (self.key == "text"):
          text_id = "textInput_"+id_text
          component_id = text_id
        elif (self.key == "date"):
          date_id = "date_"+id_text
          component_id = date_id
        elif (self.key == "range"):
          range_id = "range_"+id_text
          component_id = range_id
        elif (self.key == "feature-element"):
          feature_ele_id = "featured_item_"+id_text
          component_id = feature_ele_id
        elif (self.key == "mix-para"):
          para_id = "mix_para_"+id_text
          component_id = para_id
        elif (self.key == "mix-table"):
          table_id = "mix_table_"+id_text
          component_id = table_id
        elif (self.key == "mix-ordered-list"):
          ol_id = "mix_ol_"+id_text
          component_id = ol_id
        elif (self.key == "mix-unordered-list"):
          ul_id = "mix_ul_"+id_text
          component_id = ul_id
        elif (self.key in ["sidebar-title","sidebar-text","navbar-title","navbar-text","header-title","footer-title","label","carousel-title","table-col","list-item"]):
          component_id = self.key.replace("-","_")+"_text_element_"+id_text

        for child in self.children:
            if ("layout_type" in child.key):
              layout_type = child.children[0].key
              continue
            if ("auto" in child.key):
              nav_style = mapping.get(child.key)
              continue
            placeholder = ""
            if (self.key!="mix-para"):
              placeholder, script_holder = child.render(mapping, self.rendering_function, spacing+4, script_holder)
            else:
              placeholder, script_holder = child.render(mapping, self.detailed_rendering_function, spacing+4, script_holder)
            if placeholder is None:
                self = None
                return
            else:
                if ("navbar-title" in child.key):
                  nav_title_placeholder = placeholder
                elif ("sidebar-title" in child.key):
                  sidebar_title_placeholder = placeholder
                elif (child_count ==0 and "carousel-title" in child.key):
                  placeholder = placeholder.replace("<div class=\"carousel-item\">", "<div class=\"carousel-item active\">")
                  content+=placeholder
                elif ("tab-element" in child.key):
                  tab_id = "\"" + tab_title + "_"+str(child_count) + "\""
                  placeholder = placeholder.replace("??tabid??", tab_id)
                  if (child_count==0):
                    placeholder = placeholder.replace("<div class=\"tab-pane fade border p-3 show\"","<div class=\"tab-pane fade border p-3 show active\"")
                  content += placeholder
                elif ("feature-element" in child.key):
                  feature_title = SamplerUtils.get_random_text(12,3,True)
                  feature_para = SamplerUtils.get_random_text(35,6,True)
                  placeholder = placeholder.replace("[??title??]", feature_title)
                  placeholder = placeholder.replace("[??para??]", feature_para)
                  content+=placeholder
                elif ("card-item" in child.key):
                  card_title = SamplerUtils.get_random_text(12,3,True)
                  card_para = SamplerUtils.get_random_text(50,10,True)
                  card_button = SamplerUtils.get_random_text()
                  placeholder = placeholder.replace("[??cardtitle??]", card_title)
                  placeholder = placeholder.replace("[??cardbody??]", card_para)
                  placeholder = placeholder.replace("[??cardbutton??]", card_button)
                  content+=placeholder
                elif ("collapse-title" in child.key):
                  collapse_title_link = collapse_id + "_"+str(child_count)
                  placeholder = placeholder.replace("??collapsetarget??", collapse_title_link)
                  placeholder = placeholder.replace("??collapsebody??", SamplerUtils.get_random_text(40,8,True))
                  content+=placeholder
                elif ("checkbox" in child.key):
                  checkbox_num = checkbox_id + "_"+str(child_count)
                  placeholder = placeholder.replace("??checkboxid??", checkbox_num)
                  content+=placeholder
                else: 
                  content += placeholder
            child_count+=1
        value = mapping.get(self.key, None)
        if value is None:
            self = None
            return None
        if rendering_function is not None:
            value = rendering_function(self.key, value)
        else:
            value = self.rendering_function(self.key, value)

        if len(self.children) != 0:
            value = value.replace(self.content_holder, content)
        if ("ul class=\"navbar-nav **\"" in value):
            value = value.replace("ul class=\"navbar-nav **\"", "ul class=\"navbar-nav " + nav_style +"\"")
        if (self.key == "navbar"):
            value = value.replace("??navtitle??",nav_title_placeholder)
        elif (self.key == "sidebar"):
            value = value.replace("??sidebartitle??",sidebar_title_placeholder)
        if (self.key=="carousel"):
          value = value.replace("[??carousel_id??]",carousel_title)
          carousel_indicators = len(self.children)
          indicator_string = "<li class=\"active\" data-slide-to=\"0\"></li>\n"
          for i in range(1, carousel_indicators):
            indicator_string+= "<li class=\"\" data-slide-to=\"" + str(i)+"\"></li>\n"
          value = value.replace("??carouselindicators??", indicator_string)
        elif (self.key=="tabs"):
          tab_navs = len(self.children)
          nav_string = "<a class=\"nav-item nav-link active\" data-toggle=\"tab\" href=\"#"+ tab_title+"_"+str(0)+"\" role=\"tab\">"+ SamplerUtils.get_random_text() + "</a>\n"
          for i in range(1, tab_navs):
              nav_string += "<a class=\"nav-item nav-link\" data-toggle=\"tab\" href=\"#"+ tab_title+"_"+str(i)+"\" role=\"tab\">"+ SamplerUtils.get_random_text() + "</a>\n"
          value = value.replace("??tabnavigation??", nav_string)
        elif (self.key=="text"):
          value = value.replace("??text_id??",text_id)
        elif (self.key=="date"):
          value = value.replace("??date_id??",date_id)
        elif (self.key=="range"):
          value = value.replace("??range_id??",range_id)
        elif (self.key=="feature-element"):
          value = value.replace("??feature_ele_id??",feature_ele_id)
        elif (self.key=="mix-para"):
          value = value.replace("??para_id??",para_id)
        elif (self.key=="mix-table"):
          value = value.replace("??table_id??",table_id)
        elif (self.key=="mix-ordered-list"):
          value = value.replace("??ol_id??",ol_id)
        elif (self.key=="mix-unordered-list"):
          value = value.replace("??ul_id??",ul_id)

        if (self.key in ["header", "footer","navbar","sidebar","text","date","range","feature-element","mix-para","mix-table","mix-ordered-list","mix-unordered-list","carousel"]):
          bgcolorpicker  = mapping.get("bgcolor-picker")
          modifiers = ""
          if (self.key == "header"):
            component_id = "header-wrapper"
          elif (self.key == "footer"):
            component_id = "footer-wrapper"
          elif (self.key=="navbar"):
            component_id = "navbar-wrapper"
          elif (self.key=="sidebar"):
            component_id = "sidebar-wrapper"
          elif (self.key=="carousel"):
            component_id = carousel_title
          # if ("insert_parent" in value):
              # print(self.key, value, component_id)
              # value = value.replace("insert_parent",component_id)
          bgcolorpicker_id = "bgcolorpicker_"+component_id
          bgcolorpicker = bgcolorpicker.replace("??bgcolorpicker_id??",bgcolorpicker_id)
          bgcolorpicker = bgcolorpicker.replace("??btn_bgcolor_id??","button_"+bgcolorpicker_id)
          bgcolorpicker_fn_script = bgcolorpicker_id.replace("-","_")
          bgcolorpicker_fn_btn_script = "button_"+bgcolorpicker_id.replace("-","_")
          bgcomponent_fn_script = component_id.replace("-","_")
          bg_scriptid = "\n\nfunction "+bgcolorpicker_fn_btn_script+"_func(event){\ninput = document.getElementById(\"bgcolorpicker_"+component_id+"\")\ninput.click()\nevent.preventDefault()\n}\nbg_btn = document.getElementById(\"button_"+bgcolorpicker_id+"\")\nbg_btn.addEventListener('click',"+bgcolorpicker_fn_btn_script+"_func)\n\nfunction "+bgcolorpicker_fn_script+"_func(event){\ncolor = document.getElementById(\""+bgcolorpicker_id+"\")\ndocument.getElementById(\""+component_id+"\").style.setProperty('background-color', color.value,'important')\nchanges."+bgcolorpicker_fn_script+"_bgcolor= color.value\nevent.preventDefault()\n}\ncolor = document.getElementById(\""+bgcolorpicker_id+"\")\ncolor.addEventListener(\"change\","+bgcolorpicker_fn_script+"_func)\n"
          modifiers += bgcolorpicker
          script_holder+= bg_scriptid

          fgcolorpicker = mapping.get("fgcolor-picker")
          # modifiers = ""
          ##IF key in text, date , range - set the bgcolor and fgcolor to the corr label.
          fgcolorpicker_id = "fgcolorpicker_"+component_id
          fgcolorpicker = fgcolorpicker.replace("??fgcolorpicker_id??",fgcolorpicker_id)
          fgcolorpicker = fgcolorpicker.replace("??btn_fgcolor_id??","button_"+fgcolorpicker_id)
          fgcolorpicker_fn_script = fgcolorpicker_id.replace("-","_")
          fgcolorpicker_fn_btn_script = "button_"+fgcolorpicker_id.replace("-","_")
          fgcomponent_fn_script = component_id.replace("-","_")
          fg_scriptid = "\n\nfunction "+fgcolorpicker_fn_btn_script+"_func(event){\ninput = document.getElementById(\"fgcolorpicker_"+component_id+"\")\ninput.click()\nevent.preventDefault()\n}\nfg_btn = document.getElementById(\"button_"+fgcolorpicker_id+"\")\nfg_btn.addEventListener('click',"+fgcolorpicker_fn_btn_script+"_func)\n\nfunction "+fgcolorpicker_fn_script+"_func(event){\ncolor = document.getElementById(\""+fgcolorpicker_id+"\")\ndocument.getElementById(\""+component_id+"\").style.setProperty('color', color.value,'important')\nchanges."+fgcolorpicker_fn_script+"_fgcolor= color.value\nevent.preventDefault()\n}\ncolor = document.getElementById(\""+fgcolorpicker_id+"\")\ncolor.addEventListener(\"change\","+fgcolorpicker_fn_script+"_func)\n"
          modifiers += fgcolorpicker
          script_holder+= fg_scriptid
          value = value.replace("[??modifiers??]",modifiers)
        
          if (self.key =="feature-element"):
            # print(value, component_id)
            # feature_title = SamplerUtils.get_random_text(12,3,True)
            # value = value.replace("[??title??]", feature_title)
            imageModifier = ""
            imgpicker = mapping.get("img-picker")
            btn_id = "img_button_"+feature_ele_id
            closer_id = "img_closer_"+feature_ele_id
            modal_id = "img_modal_"+feature_ele_id
            feature_span_id = "img_span_"+feature_ele_id
            upload_id = "imgUpload_"+feature_ele_id
            caption_id ="imgGenerateCaption_"+feature_ele_id
            generate_btn_id = "imgGenerate_"+feature_ele_id
            gen_img_display_id = "imgGenerateDisplay_"+feature_ele_id
            gen_img1 = "generated_image_1_"+feature_ele_id
            gen_img2 = "generated_image_2_"+feature_ele_id
            gen_img3 = "generated_image_3_"+feature_ele_id
            gen_img4 = "generated_image_4_"+feature_ele_id
            gen_img1_src = "../static/images/"+gen_img1
            gen_img2_src = "../static/images/"+gen_img2
            gen_img3_src = "../static/images/"+gen_img3
            gen_img4_src = "../static/images/"+gen_img4

            img_loader_id = "imgLoader_"+feature_ele_id
            text_span_id = "text_span_"+feature_ele_id

            value = value.replace("??feature_span_id??", feature_span_id)
            imgpicker = imgpicker.replace("??imgpicker_id??",btn_id)
            imgpicker = imgpicker.replace("??imgModal_id??",modal_id)
            imgpicker = imgpicker.replace("??imgmodalcloser_id??",closer_id)
            imgpicker = imgpicker.replace("??featureupload_id??",upload_id)
            imgpicker = imgpicker.replace("??featuregenerate_id??",caption_id)
            imgpicker = imgpicker.replace("??generate_caption_btn_id??",generate_btn_id)
            imgpicker = imgpicker.replace("??gen_img_display??",gen_img_display_id)
            imgpicker = imgpicker.replace("??gen_image_1??",gen_img1)
            imgpicker = imgpicker.replace("??gen_image_2??",gen_img2)
            imgpicker = imgpicker.replace("??gen_image_3??",gen_img3)
            imgpicker = imgpicker.replace("??gen_image_4??",gen_img4)
            imgpicker = imgpicker.replace("??img_gen_loader??",img_loader_id)

            imageModifier += imgpicker
            toggleScriptHeader = "toggle_img_modal_"+feature_ele_id+"_func"
            addImageHeader = "add_image_"+feature_ele_id+"_func"
            generateImageHeader = "generate_image_"+feature_ele_id+"_func"
            img_script = "\n\nfunction "+toggleScriptHeader+"(event){\nmodal = document.getElementById(\""+modal_id+"\")\nif(modal.style.display==\"block\"){\nmodal.style.display = \"none\"\nimageModal=document.getElementById(\""+gen_img_display_id+"\")\nimageModal.style.display=\"none\"\n}\nelse{\nmodal.style.display =\"block\"\n}\nevent.preventDefault()\n}\n\nfunction "+addImageHeader+"(event){\nvar files = document.getElementById(\""+upload_id+"\").files\nimg = document.getElementById(\""+feature_span_id+"\")\nif (files.length > 0){\nfile = files[0]\n"\
                          +"img.style.background = \"url(\"+URL.createObjectURL(file)+\")\"\nimg.style.backgroundPosition = \"50% 50%\"\nimg.style.backgroundSize = \"cover\"\nchanges.imgpicker_"+feature_span_id+"_src=file.name\nvar formData = new FormData()\nformData.append(\"file\",file)\nvar request = new XMLHttpRequest()\nrequest.open(\"POST\", \"/upload-feature-image\")\nrequest.send(formData)\n}\nelse{\n img.style.background = \"none\"\nimg.style.backgroundColor=\"rgb(189,189,189)\"\n"\
                          +"changes."+feature_span_id+"_src=null\n}\nevent.preventDefault();\n}\ncloser = document.getElementById(\""+closer_id+"\")\nopener = document.getElementById(\""+btn_id+"\")\nimgupl = document.getElementById(\""+upload_id+"\")\nimgupl.addEventListener(\"change\","+ addImageHeader+")\ncloser.addEventListener(\"click\","+toggleScriptHeader+")\nopener.addEventListener(\"click\","+ toggleScriptHeader+")\n"\
                          +"function "+generateImageHeader+"(event){\ntext=document.getElementById(\""+caption_id+"\")\nvar formData = new FormData()\nformData.append(\"image_caption\",text.value)\nformData.append(\"ele_id\",\""+feature_ele_id+"\")\n"\
                          +"var request = new XMLHttpRequest()\nrequest.onload = function (e) {\nif (request.readyState === 4) {\nif (request.status === 200) {\nconsole.log(request.response)\nimageModal=document.getElementById(\""+gen_img_display_id+"\")\nimageModal.style.display=\"block\"\ncloser = document.getElementById(\""+closer_id+"\")\ncloser.disabled=false\ncaptionbtn = document.getElementById(\""+generate_btn_id+"\")\ncaptionbtn.disabled=false\nloaderModal=document.getElementById(\""+img_loader_id+"\")\nloaderModal.style.display=\"none\"\n"\
                          +"timestamp=request.response\nimg1=document.getElementById(\""+gen_img1+"\")\nimg2=document.getElementById(\""+gen_img2+"\")\nimg3=document.getElementById(\""+gen_img3+"\")\nimg4=document.getElementById(\""+gen_img4+"\")\nimg1.src=\""+gen_img1_src+"_\"+timestamp+\".jpg\"\nimg2.src=\""+gen_img2_src+"_\"+timestamp+\".jpg\"\nimg3.src=\""+gen_img3_src+"_\"+timestamp+\".jpg\"\nimg4.src=\""+gen_img4_src+"_\"+timestamp+\".jpg\"\n}\n}\n}\nloaderModal=document.getElementById(\""+img_loader_id+"\")\nloaderModal.style.display=\"block\"\ncloser = document.getElementById(\""+closer_id+"\")\ncloser.disabled=true\ncaptionbtn = document.getElementById(\""+generate_btn_id+"\")\ncaptionbtn.disabled=true\nimg1=document.getElementById(\""+gen_img1+"\")\nimg2=document.getElementById(\""+gen_img2+"\")\nimg3=document.getElementById(\""+gen_img3+"\")\nimg4=document.getElementById(\""+gen_img4+"\")\nimg1.src=\"\"\nimg2.src=\"\"\nimg3.src=\"\"\nimg4.src=\"\"\nimageModal=document.getElementById(\""+gen_img_display_id+"\")\nimageModal.style.display=\"none\"\ncaption=document.getElementById(\""+text_span_id+"\")\ncaption.innerHTML = text.value\nchanges.textpicker_"+text_span_id+"_caption=text.value\nrequest.open(\"POST\", \"/generate-images-for-text\")\nrequest.send(formData)\nevent.preventDefault()\n}\n"\
                          +"captionbtn = document.getElementById(\""+generate_btn_id+"\")\ncaptionbtn.addEventListener(\"click\","+generateImageHeader+")\n"\
                          +"\n\nfunction click_gen_img_to_src_"+feature_ele_id+"_func(event){\nid=event.target.id\nimg = document.getElementById(\""+feature_span_id+"\")\nimg_src=document.getElementById(id).src\nimg.style.background = \"url(\"+img_src+\")\"\nimg.style.backgroundPosition = \"50% 50%\"\nimg.style.backgroundSize = \"cover\"\nchanges.imgpicker_"+feature_span_id+"_src=img_src.split('/').pop()\nevent.preventDefault()\n}\nimg1=document.getElementById(\""+gen_img1+"\")\nimg2=document.getElementById(\""+gen_img2+"\")\nimg3=document.getElementById(\""+gen_img3+"\")\nimg4=document.getElementById(\""+gen_img4+"\")\n"\
                          +"img1.addEventListener('click',click_gen_img_to_src_"+feature_ele_id+"_func)\nimg2.addEventListener('click',click_gen_img_to_src_"+feature_ele_id+"_func)\nimg3.addEventListener('click',click_gen_img_to_src_"+feature_ele_id+"_func)\nimg4.addEventListener('click',click_gen_img_to_src_"+feature_ele_id+"_func)\n"
            script_holder+=img_script
            value = value.replace("[??imageModifier??]",imageModifier)
          # modifiers = modifiers.replace("\n","\n"+(" "*spacing))
        if (self.key in ["sidebar-title","sidebar-text","navbar-title","navbar-text","header-title","footer-title","label","carousel-title","table-col","list-item","feature-element"]):
            text_editor = mapping.get("text-editor")
            if (self.key in ["carousel-title"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"","style=\"display:none; z-index: 1;width:200px;overflow: auto; left:45%; position:relative;height:100px\"")
            elif (self.key in ["feature-element"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"","style=\"display:none; z-index: 1;width:200px;overflow: auto; left:90px;top:260px; position:absolute;height:100px\"")
            elif (self.key in ["header-title"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"","style=\"display:none; z-index: 1;width:200px;overflow: auto; top:60px; position:relative;height:100px\"")
            elif (self.key in ["footer-title"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"","style=\"display:none; z-index: 1;width:200px;overflow: auto; top:30px; position:relative;height:100px\"")
            elif (self.key in ["label"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"","style=\"display:none; z-index: 1;width:200px;overflow: auto; top:-30px; left:120px; height:100px; position:relative;\"")
            elif (self.key in ["navbar-title","navbar-text"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"","style=\"display:none; z-index: 1;width:200px;overflow: auto; top:40px; left:170px; position:absolute;height:100px\"")
            elif (self.key in ["list-item"]):
              text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"", "style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px; top:-30px; left:200px;\"")
            # elif (self.key in ["sidebar-title", "sidebar=text"]):
              # text_editor = text_editor.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto;position:relative;height:100px\"", "style=\"display:none; z-index: 1;width:200px;overflow: auto;position:absolute;height:100px; top:45px; left:100px;\"")
            
            btn_id = "text_button_"+component_id
            closer_id = "text_closer_"+component_id
            modal_id = "text_modal_"+component_id
            text_span_id = "text_span_"+component_id
            textEdit_id = "textEdit_"+component_id
            value = value.replace("textModifiedId", text_span_id)
            text_editor = text_editor.replace("??textpicker_id??",btn_id)
            text_editor = text_editor.replace("??textModal_id??",modal_id)
            text_editor = text_editor.replace("??textmodalcloser_id??",closer_id)
            text_editor = text_editor.replace("??text_edit_id??",textEdit_id)
            modifiers = text_editor
            toggleScriptHeader = "toggle_text_modal_"+component_id+"_func"
            addTextHeader = "add_text_"+component_id+"_func"
            text_script = "\n\nfunction "+toggleScriptHeader+"(event){\nmodal = document.getElementById(\""+modal_id+"\")\nif(modal.style.display==\"block\"){\nmodal.style.display = \"none\"\n}\nelse{\nmodal.style.display =\"block\"\n}\nevent.preventDefault()\n}\n\nfunction "+addTextHeader+"(event){\nvar text = document.getElementById(\""+textEdit_id+"\").value\ncaption = document.getElementById(\""+text_span_id+"\")\ncaption.innerHTML = text\nchanges.textpicker_"+text_span_id+"_caption=text\nevent.preventDefault();\n}\ncloser = document.getElementById(\""+closer_id+"\")\nopener = document.getElementById(\""+btn_id+"\")\nimgupl = document.getElementById(\""+textEdit_id+"\")\nimgupl.addEventListener(\"change\","+ addTextHeader+")\ncloser.addEventListener(\"click\","+toggleScriptHeader+")\nopener.addEventListener(\"click\","+ toggleScriptHeader+")\n"
            script_holder+=text_script 
            value = value.replace("[??textModifier??]",modifiers)
        if (self.key == "mix-para"):
          #Replace label modifier style
          value = value.replace("style=\"display:none; z-index: 1;width:200px;overflow: auto; top:-30px; left:120px; height:100px; position:relative;\"", "style=\"display:none; z-index: 1;width:200px;overflow: auto; height:100px; position:relative;\"")

        if (self.key == "body"):
          value = value.replace("[??body_script??]", script_holder)

        if (layout_type == "layout_1"):
          # Dflex on full-wrapper w-100 on [header+navbar, content, footer]
          value = value.replace("<div class=\"bg-gradient bg-light\" id=\"full-wrapper\">","<div class=\"bg-gradient bg-light d-flex\" id=\"full-wrapper\">")
          insert_index1 = value.find("<header")
          insert_index2 = value.find("<nav")

          if (insert_index1 == -1 and insert_index2 ==-1):
            insert_index = value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")
          elif (insert_index1 == -1):
            insert_index = insert_index2
          elif (insert_index2 == -1):
            insert_index = insert_index1
          elif (insert_index1<insert_index2):
            insert_index = insert_index1
          else:
            insert_index = insert_index2
          value = value[:insert_index] + "<div class=\"w-100\">\n"+value[insert_index:]
          end_index = value.find("</body>")
          sidebar_index = value.find("<div class=\"bg-gradient bg-light shadow\" data-wg-type=\"sidebar\" id=\"sidebar-wrapper\">")
          if (sidebar_index > insert_index and sidebar_index!=-1):
              end_index = sidebar_index
          value = value[:end_index] + "\n</div>\n"+value[end_index:]

        elif (layout_type == "layout_2"):
          #d_flex after header + navbar, flex_grow_1 or container fluid 3 on content
          insert_index = value.find("<div class=\"bg-gradient bg-light shadow\" data-wg-type=\"sidebar\" id=\"sidebar-wrapper\">")
          if (insert_index > value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")):
            insert_index = -1
          if (insert_index == -1):
            insert_index = value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")
          value = value[:insert_index] + "<div class=\"d-flex\">\n"+value[insert_index:] 
          end_index = value.find("</body>")
          value = value[:end_index] + "\n</div>\n"+value[end_index:]

          footer_index = value.find("<footer")
          if (footer_index !=-1):
            insert_index = value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")
            value = value[:insert_index] + "<div class=\"flex-grow-1\">\n"+value[insert_index:]
            end_index = value.find("/footer>")
            value =  value[:end_index+8]+ "\n</div>\n"+value[end_index+8:]
 
        elif (layout_type == "layout_3"):
          insert_index = value.find("<div class=\"bg-gradient bg-light shadow\" data-wg-type=\"sidebar\" id=\"sidebar-wrapper\">")
          if (insert_index > value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")):
            insert_index = -1
          if (insert_index == -1):
            insert_index = value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")
          value = value[:insert_index]+ "<div class=\"d-flex\">\n"+value[insert_index:] 
          end_index = value.find("</body>")
          if (value.find("<footer")!=-1):
            end_index = value.find("<footer")
          value = value[:end_index]+ "\n</div>\n"+value[end_index:]
        
        elif (layout_type == "layout_4"):
          insert_index = value.find("<div class=\"bg-gradient bg-light shadow\" data-wg-type=\"sidebar\" id=\"sidebar-wrapper\">")
          sidebar_first = True
          if (insert_index > value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")):
            insert_index = -1
            sidebar_first = False
          if (insert_index == -1):
            insert_index1 = value.find("<header")
            insert_index2 = value.find("<nav")

            if (insert_index1 == -1 and insert_index2 ==-1):
              insert_index = value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")
            elif (insert_index1 == -1):
              insert_index = insert_index2
            elif (insert_index2 == -1):
              insert_index = insert_index1
            elif (insert_index1<insert_index2):
              insert_index = insert_index1
            else:
              insert_index = insert_index2
          value = value[:insert_index] + "<div class=\"d-flex\">\n"+value[insert_index:] 
          end_index = value.find("</body>")
          if (value.find("<footer")!=-1):
            end_index = value.find("<footer")
          value = value[:end_index]+ "\n</div>\n"+value[end_index:]

          insert_index1 = value.find("<header")
          insert_index2 = value.find("<nav")

          if (insert_index1 == -1 and insert_index2 ==-1):
            insert_index = value.find("<div class=\"container-fluid py-3\" id=\"page-content\">")
          elif (insert_index1 == -1):
              insert_index = insert_index2
          elif (insert_index2 == -1):
              insert_index = insert_index1
          elif (insert_index1<insert_index2):
            insert_index = insert_index1
          else:
            insert_index = insert_index2
          value = value[:insert_index]+ "<div class=\"w-100\">\n"+value[insert_index:] 
          
          end_index = value.find("</body>")
          if (value.find("<footer")!=-1):
            end_index = value.find("<footer")
          sidebar_index = value.find("<div class=\"bg-gradient bg-light shadow\" data-wg-type=\"sidebar\" id=\"sidebar-wrapper\">")
          if (not sidebar_first and sidebar_index!=-1):
            end_index = sidebar_index
          value = value[:end_index] + "\n</div>\n"+value[end_index:]
        
        if (self.key=="body"):
          index= value.index("</body>")
          value = value[:index]+ "<!--START OF REMOVAL SECTION-->\n<div class=\"row\">\n<input class=\"color-picker\" type=\"color\" style=\"visibility:hidden;display:flex;height:0px;width:0px;\"  id=\"bgcolorpicker_body\"/>\n<button class=\"button\" style=\"width: 150px;height:50px;\" id = \"btnbgcolor_body\">\nSet Body BGColor\n</button>\n</div>\n"\
          +"<div class=\"row\">\n"\
          + "&nbsp;&nbsp;"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_1\" style=\"width:30px;height:30px;\">\n1\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_2\" style=\"width:30px;height:30px;\">\n2\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_3\" style=\"width:30px;height:30px;\">\n3\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_4\" style=\"width:30px;height:30px;\">\n4\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_5\" style=\"width:30px;height:30px;\">\n5\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_6\" style=\"width:30px;height:30px;\">\n6\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_7\" style=\"width:30px;height:30px;\">\n7\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_8\" style=\"width:30px;height:30px;\">\n8\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_9\" style=\"width:30px;height:30px;\">\n9\n</button>\n"\
          +"<button type=\"button\" class=\"button\" id=\"preset_btn_10\" style=\"width:30px;height:30px;\">\n10\n</button>\n"\
          +"</div>\n<!--END OF REMOVAL SECTION-->\n"\
          +value[index:]

          preset_functions = "function preset1_function(event){\nfirst = \"#F3EFE2\"\nsecond = \"#9D9282\"\nmiddle = \"#BF6A32\"\nsecond_last = \"#976F56\"\nlast = \"#332C30\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc1_btn = document.getElementById(\"preset_btn_1\")\nc1_btn.addEventListener(\"click\",preset1_function)\n"\
          +"function preset2_function(event){\nfirst = \"#F9F8F8\"\nsecond = \"#8C9081\"\nmiddle = \"#34E1BA\"\nsecond_last = \"#7A5D60\"\nlast = \"#1F4F8C\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc2_btn = document.getElementById(\"preset_btn_2\")\nc2_btn.addEventListener(\"click\",preset2_function)\n"\
          +"function preset3_function(event){\nfirst = \"#F2F2EB\"\nsecond = \"#87A7A1\"\nmiddle = \"#B1BF32\"\nsecond_last = \"#A35E3A\"\nlast = \"#2A3C37\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc3_btn = document.getElementById(\"preset_btn_3\")\nc3_btn.addEventListener(\"click\",preset3_function)\n"\
          +"function preset4_function(event){\nfirst = \"#ECEEE9\"\nsecond = \"#748C81\"\nmiddle = \"#779A7E\"\nsecond_last = \"#386F44\"\nlast = \"#1A1F20\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc4_btn = document.getElementById(\"preset_btn_4\")\nc4_btn.addEventListener(\"click\",preset4_function)\n"\
          +"function preset5_function(event){\nfirst = \"#EFEFF0\"\nsecond = \"#7C7A89\"\nmiddle = \"#508DBD\"\nsecond_last = \"#384A6F\"\nlast = \"#1B161F\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc5_btn = document.getElementById(\"preset_btn_5\")\nc5_btn.addEventListener(\"click\",preset5_function)\n"\
          +"function preset6_function(event){\nfirst = \"#F7F3F3\"\nsecond = \"#D46F6C\"\nmiddle = \"#4B8095\"\nsecond_last = \"#A64632\"\nlast = \"#20141E\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc6_btn = document.getElementById(\"preset_btn_6\")\nc6_btn.addEventListener(\"click\",preset6_function)\n"\
          +"function preset7_function(event){\nfirst = \"#120E11\"\nsecond = \"#212EA8\"\nmiddle = \"#4697CA\"\nsecond_last = \"#6B769A\"\nlast = \"#ECDFDD\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc7_btn = document.getElementById(\"preset_btn_7\")\nc7_btn.addEventListener(\"click\",preset7_function)\n"\
          +"function preset8_function(event){\nfirst = \"#202924\"\nsecond = \"#368157\"\nmiddle = \"#5C9A98\"\nsecond_last = \"#6D8B7F\"\nlast = \"#E8E9E1\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc8_btn = document.getElementById(\"preset_btn_8\")\nc8_btn.addEventListener(\"click\",preset8_function)\n"\
          +"function preset9_function(event){\nfirst = \"#28146F\"\nsecond = \"#5A6BA5\"\nmiddle = \"#736786\"\nsecond_last = \"#8AA3BB\"\nlast = \"#E2E3CB\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc9_btn = document.getElementById(\"preset_btn_9\")\nc9_btn.addEventListener(\"click\",preset9_function)\n"\
          +"function preset10_function(event){\nfirst = \"#3A4155\"\nsecond = \"#3AA44A\"\nmiddle = \"#7D887E\"\nsecond_last = \"#919EA2\"\nlast = \"#EAEBE5\"\nset_preset_function(first,second,middle,second_last,last)\n}\nc10_btn = document.getElementById(\"preset_btn_10\")\nc10_btn.addEventListener(\"click\",preset10_function)\n"

          value = value.replace("[??add_preset_functions??]",preset_functions)
          spacing = 0
          value_list = value.split("\n")
          for item in range(1,len(value_list)):
            if (value_list[item]=="}"):
              
              value_list[item] = " "*spacing + value_list[item]
              spacing-=4
            elif (len(value_list[item])<2):
              continue
            elif (value_list[item][0:5] in ["</div","</bod","</hea","</nav","</foo","</tr>"]):
              value_list[item] = " "*spacing + value_list[item]
              spacing -=4
            elif (value_list[item][0:4] in ["<div","<bod","<hea","<nav","<foo","func","else","<tr>","for","if"] or value_list[item][0:2]=="if"):
              spacing +=4
              value_list[item] = " "*spacing + value_list[item]
            elif (value_list[item]=="<script id=\"dynamic_script\">"):
              spacing+=4
              value_list[item] = " "*spacing + value_list[item]
            elif (value_list[item]=="</script>"):
              spacing-=4
              value_list[item] = " "*spacing + value_list[item]
            else:
              value_list[item] = " "*(spacing+4) + value_list[item]
          value = "\n".join(value_list)
         
        return value, script_holder