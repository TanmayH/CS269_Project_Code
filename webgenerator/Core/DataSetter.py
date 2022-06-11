from Core.WebGenerator import WebGenerator
from Core.ScreenShutter import ScreenShutter
from Core.FileManager import FileManager 
import time
import os
import copy

class DataSetter:
	def __init__(self, webgen: WebGenerator, screen_shutter: ScreenShutter=None, delete_previous_files: bool=True):
		self.webgen = webgen
		self.screen_shutter = screen_shutter
		self.delete_previous_files = delete_previous_files
	
	def write_to_gui_file(self, layout_list,file_num):
		for component in layout_list:
			print(component)
		print ("\n\n")
		output_path = os.path.join(self.webgen.output_path, "gui")
		gui_string = ""
		for component in layout_list:
			key = [a for a in component][0]
			value = component[key]

			if (key=="layout_type"):
				gui_string += key + "{ \n" + value + "\n}\n"
			elif (key in ["sidebar","header","navbar","footer"]):
				gui_string += key + "{ \n"
				for content in value:
					gui_string += content + ", "
				gui_string = gui_string[:-2]
				gui_string += "\n}\n" 
			elif (key=="content-form"):
				gui_string += key + "{ \n"
				for row in value:
					inner_key = [b for b in row][0]
					inner_value = row[inner_key]
					gui_string += inner_key + "{ \n"
					for content in inner_value:
						inner_content_key = [c for c in content][0]
						inner_content_value = content[inner_content_key]
						gui_string += inner_content_key + "{ \n"
						for inner_content in inner_content_value:
							gui_string += inner_content + ", "
						gui_string = gui_string[:-2]
						gui_string += "\n}\n"
					gui_string += "}\n" 
				gui_string += "}\n" 
			elif (key=="content-section"):
				gui_string += key + "{ \n"
				for row in value:
					inner_key = [b for b in row][0]
					inner_value = row[inner_key]
					gui_string += inner_key + "{ \n"
					if (inner_key != "mixed-single" and inner_key!="mixed-double"):
					# if (inner_key != "mixed"):
						for content in inner_value:
							gui_string += content + ", "
						gui_string = gui_string[:-2]
						gui_string += "\n}\n"
					else:
						for content in inner_value:
							inner_content_key = [c for c in content][0]
							inner_content_value = content[inner_content_key]
							gui_string += inner_content_key + "{ \n"
							if (inner_content_key!="mix-table"):
								for inner_content in inner_content_value:
									gui_string += inner_content + ", "
								gui_string = gui_string[:-2]
								gui_string += "\n}\n"
							else:
								for table_content in inner_content_value:
									table_key = [c for c in table_content][0]
									table_value = table_content[table_key]

									# print (content, inner_content_key, inner_content_value)
									gui_string += table_key + "{ \n"
									for inner_table_content in table_value:
										gui_string += inner_table_content + ", "
									gui_string = gui_string[:-2]
									gui_string += "\n}\n"
								gui_string += "}\n" 
						gui_string += "}\n" 
				gui_string += "}\n" 
				
		with open(os.path.join(output_path, "rw_"+str(file_num)+".gui"), 'a') as convert_file:
			convert_file.write(gui_string)

	def batch(self,n_files,with_annotations=None, 
		with_color_variation=None, output_path=None,start_id =0):
		with_annotations, with_color_variation, output_path = self.load_defaults_if_none(
			with_annotations=self.webgen.with_annotations,
			with_color_variation=self.webgen.with_color_variation, 
			output_path = self.webgen.output_path
		)

		FileManager.prepare_output(output_path, self.delete_previous_files, with_annotations)

		#Generate HTML
		tic = time.time()
		count = 0
		for i in range(start_id,n_files+start_id):
			website = self.webgen.generate(with_annotations=True, with_color_variation=True) 
			orig_website = copy.deepcopy(website)
			orig_website.head[-1]="" 
			FileManager.save(os.path.join(output_path,"html/rw_"+str(i)+"sketch.html"),website.render())
			FileManager.save(os.path.join(output_path,"html/rw_"+str(i)+".html"),orig_website.render())
			count += 1
			self.write_to_gui_file(website.layout_list, i)

		tac = time.time()
		print("Generated {0} HTML files in {1} seconds. Files are in {2}.".format(count,round(tac-tic, 1),self.webgen.output_path))

		#Generate Screenshots
		if self.screen_shutter is not None:
			self.screen_shutter.capture_and_save() #Skip generation of ss for non-sketch. And bunch into a single folder sketch and gui file. 

	def load_defaults_if_none(self,**kwargs):
		for key, value in kwargs.items():
			if value is not None:
				yield value
			else:
				yield getattr(self.webgen,key)
