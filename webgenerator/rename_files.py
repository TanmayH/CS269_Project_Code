import os

for filename in os.listdir("D:\Desktop\cs269_new_simplified_data"):
    if "sketch" in filename:
        # print (filename)
        sketch_index = filename.find("sketch")
        new_filename = filename[0:sketch_index]+".png"
        os.rename(os.path.join("D:\Desktop\cs269_new_simplified_data",filename),os.path.join("D:\Desktop\cs269_new_simplified_data",new_filename))