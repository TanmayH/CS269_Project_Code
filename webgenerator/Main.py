from Randomization.WebLayout import WebLayoutProbabilities
from Core.WebGenerator import WebGenerator
from Core.ScreenShutter import ScreenShutter
from Core.DataSetter import DataSetter
from html2image import Html2Image
class Main:
	def run():
		# Set probabilities and settings
		# self,with_sidebar_p, with_header_p, with_navbar_p, with_footer_p, 
    	# layouts_p, boxed_body_p, generate_alert_p, big_header_p, sidebar_first_p, 
		# navbar_first_p, bg_color_classes_p
		with_sidebar_p = 0.5
		with_header_p = 0.5
		with_navbar_p = 0.5
		with_footer_p = 0.5
		sidebar_first_p = 1
		navbar_first_p = 1
		layout_p = WebLayoutProbabilities(with_sidebar_p,with_header_p,with_navbar_p,with_footer_p,None,None,None,None,sidebar_first_p,navbar_first_p,None)
		generator = WebGenerator(layout_p, with_annotations=True, with_color_variation=True)

		# Generate one webpage
		generator.generate_and_save_single()


		# file = open('D:\Desktop\webgenerator\output\gui\\random_webpage.gui', 'r')
		# texts = file.read()
		# file.close()
		# syntax = '<START> ' + texts + ' <END>'
		# syntax = ' '.join(syntax.split())
		# syntax = syntax.replace(',', ' ,')
		# syntax = syntax.replace('{',' {') #newly added for purpose of how gui is written
		# print(syntax)
		# text.append(syntax)


		# # # # Set screenshots settings  
		screen_shutter = ScreenShutter(full_screenshot=True, window_size=(1500,720), driver_path ="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

		# # # Generate multiple webpages and screenshots
		data_setter = DataSetter(generator, screen_shutter, delete_previous_files=False)
		# data_setter.batch(300,start_id=0)
		# data_setter.batch(600,start_id=300)
		data_setter.batch(1000,start_id=3000)
		# data_setter.batch(600,start_id=1500)
		# data_setter.batch(600,start_id=2100)
		# data_setter.batch(300,start_id=2700)

		# data_setter.batch(300,start_id=1800)
		# data_setter.batch(300,start_id=2100)
		# data_setter.batch(300,start_id=2400)
		# data_setter.batch(300,start_id=2700)


Main.run()