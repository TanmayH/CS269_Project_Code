from random import choices
import random
import dominate # https://github.com/Knio/dominate
from dominate.tags import *
from dominate.util import raw
from lorem import * # https://github.com/JarryShaw/lorem#usage
from utils import *
from dominate import document
from dominate import dom_tag 
from Layout.HtmlComponent import EmptyHtmlComponent
from Core.DominateExtensions import DominateExtensions

class WebLayout(document):
	def __init__(self,boxed_body,layout,sidebar_first,navbar_first,force_sizes=None):
		super().__init__(title='Dominate', doctype='<!DOCTYPE html>', request=None)
		self.wrapper = self.body.add(div(id="full-wrapper"))
		DominateExtensions.bound_add_class(self.wrapper)
		DominateExtensions.bound_add_class(self.body)
		self.boxed_body = boxed_body
		self.layout = layout
		self.sidebar_first = True #changing to fixed 
		self.navbar_first = True #changing to fixed
		self.force_sizes = force_sizes
		self._header = EmptyHtmlComponent()
		self.navbar = EmptyHtmlComponent()
		self.sidebar = EmptyHtmlComponent()
		self._footer = EmptyHtmlComponent()

		self.layout_list = []
		self.layout_detail = []
	
	def build(self):
		#doc = dominate.document(title='Result')
		with self.head:
			meta(name="viewport", content="width=device-width, initial-scale=1.0")
			meta(name="author", content="Web Generator")
			meta(name="wg-layout", content=str(self.layout))
			link(rel='stylesheet', href='../css/custom-bootstrap.css')
			link(rel='stylesheet', href='../css/wg-extras.css')
			link(rel='stylesheet', href="https://fonts.googleapis.com/css?family=Schoolbell&v1")
			link(rel='stylesheet',href="https://use.fontawesome.com/releases/v5.8.1/css/all.css")
			# script(src="https://code.jquery.com/jquery-3.2.1.slim.min.js", integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN", crossorigin="anonymous")
			script(type='text/javascript', src="../js/jquery-3.2.1.slim.min.js")
			script(type='text/javascript', src='../js/bootstrap.min.js')
			comment("Layout: "+str(self.layout))
			style("""\n
			body{font-family: Schoolbell;}  
    		.bg-light,.bg-secondary,.bg-dark,.bg-primary,.bg-gradient-secondary, .bg-gradient-primary, footer, header, .btn-primary, .placeholder, .text-white, .d-block, .nav-link, table, td, tr, .bg-gradient, .bg-gradient-light, .bg-gradient-dark, .text-muted, .jumbotron{background-color: white !important; color: black!important;background-image: none !important;}
			#sidebar-wrapper, nav, footer, header, .card , .carousel, .carousel-indicators li, .border, table, .nav-tabs a, .rounded, .nav-item .nav-link, .nav-link{border: 2px solid black !important;border-top-left-radius: 30em 5em !important;border-top-right-radius: 2em 10em !important;border-bottom-right-radius: 255em 5em !important;border-bottom-left-radius:4em 25em !important;;box-shadow: 0.5px 0px 0.2em black , 0px 0.6px 0.2em black!important;}
			td{border: 2px solid black !important;box-shadow: 0.5px 0px 0.2em black , 0px 0.6px 0.2em black!important;}
			.list-group-item{border-bottom: 2px solid black ;}
			.rounded-circle, .placeholder{border: 2px solid black !important;box-shadow: 0.5px 0px 0.2em black , 0px 0.6px 0.2em black!important;}
			.card .placeholder {border: 0px solid black !important;}
			.btn, input, select{border: 1.5px solid black !important; box-shadow: 0.5px 0px 0.2em black , 0px 0.6px 0.2em black!important; color: black !important;border-top-left-radius: 30em 5em !important;border-top-right-radius: 2em 10em !important;border-bottom-right-radius: 255em 5em !important;border-bottom-left-radius:4em 25em !important;}
      		.btn2, .input2, .select3{border: 1.2px solid black !important; box-shadow: 0.7px 0.1px 0.2em black , 0px 0.6px 0.1em black!important; color: black !important;border-top-left-radius: 25em 5em !important;border-top-right-radius: 14em 8em !important;border-bottom-right-radius: 5em 8em !important;border-bottom-left-radius:24em 2em !important;}
			.btn3, .input3, .select3{border: 2.0px solid black !important; box-shadow: 0.3px 0px 0.1em black , 0.1px 0.5px 0.2em black!important;color: black !important;border-top-left-radius: 4em 25em !important;border-top-right-radius: 10em 1em !important;border-bottom-right-radius: 45em 8em !important;border-bottom-left-radius:4em 2em !important;}
			.shadow, .shadow-lg, .shadow-sm, .form-check-input{box-shadow: 0 0 0 black !important;}
			input[type=range]::-webkit-slider-thumb {box-shadow: 1px 1px 1px black;border: 1px solid black;height: 16px;width: 16px;border-radius: 15px;background: #FFFFFF;margin-top: -5px;}
			input[type=range]::-webkit-slider-runnable-track {background: white;}
			.carousel-indicators li {opacity: 1 !important;}
			.carousel-inner, .card-body {border-radius: inherit !important;}
			.carousel-control-prev, .carousel-control-next{color: black !important; font-weight: 100; background-image: none !important;}
			header, nav, .mt-0, #sidebar-wrapper{margin-top: 2em !important;}
			footer, .mb-0, #sidebar-wrapper{margin-bottom: 2em !important;}
			header, footer, nav, #sidebar-wrapper {margin-left: 1em !important;margin-right: 1em !important;}
			""")
		with self.wrapper:
			#Global margin
			if self.boxed_body is not None:
				x = self.boxed_body["x"]
				y = self.boxed_body["y"]
				if x > 5:
					self.wrapper.add_class("px-sm-5 px-3")
					self.body.add_class("px-md-"+str(x-5))
				elif x > 3:
					self.wrapper.add_class("px-sm-"+str(x)+" px-3")
				else:
					self.wrapper.add_class("px-"+str(x))

				self.wrapper.add_class("py-"+str(y))
				
			if self.has_sidebar:
				self.layout_list.append({"layout_type": "layout_"+ str(self.layout)})
				if self.layout == 1:
					if self.sidebar_first:
						if (self.has_sidebar()): 
							self.sidebar.build()
							self.layout_list.append({"sidebar":[]})
					self.wrapper.add_class('d-flex')
					main_container = div(cls="w-100")
					with main_container:  
						self.build_header_navbar()
						div(cls="container-fluid py-3", id="page-content")
						self.layout_list.append({"content":[]})
						if self.has_footer:
							self._footer.build()
							self.layout_list.append({"footer":[]})
					if not self.sidebar_first: 
						if (self.has_sidebar()): 
							self.sidebar.build()
							self.layout_list.append({"sidebar":[]})

				if self.layout == 2:
					self.build_header_navbar()
					main_container = div(cls="d-flex")
					if self.sidebar_first:
						with main_container:
							if (self.has_sidebar()): 
								self.sidebar.build()
								self.layout_list.append({"sidebar":[]})
					if self.has_footer():
						with main_container: 
							content_container = div(cls="flex-grow-1") #TODO: Rethink another easier way
							with content_container:
								div(cls="container-fluid py-3", id="page-content")
								self.layout_list.append({"content":[]})
								self._footer.build()
								self.layout_list.append({"footer":[]})
							if not self.sidebar_first:
								if (self.has_sidebar()): 
									self.sidebar.build()
									self.layout_list.append({"sidebar":[]})
					else:
						with main_container:
							div(cls="container-fluid py-3", id="page-content")
							self.layout_list.append({"content":[]})
							if not self.sidebar_first:
								if (self.has_sidebar()): 
									self.sidebar.build()
									self.layout_list.append({"sidebar":[]})

				if self.layout == 3:
					self.build_header_navbar()
					main_container = div(cls="d-flex")
					with main_container:
						if self.sidebar_first:
							if (self.has_sidebar()): 
								self.sidebar.build()
								self.layout_list.append({"sidebar":[]})
						div(cls="container-fluid py-3", id="page-content")
						self.layout_list.append({"content":[]})
						if not self.sidebar_first:
							if (self.has_sidebar()): 
								self.sidebar.build()
								self.layout_list.append({"sidebar":[]})
					if self.has_footer():
						self._footer.build()
						self.layout_list.append({"footer":[]})

				if self.layout == 4:
					main_container = div(cls="d-flex")
					with main_container:
						if self.sidebar_first:  
							if (self.has_sidebar()): 
								self.sidebar.build()
								self.layout_list.append({"sidebar":[]})
						temp_div = div(cls="w-100")
						with temp_div:
							self.build_header_navbar()
							div(cls="container-fluid py-3", id="page-content")
							self.layout_list.append({"content":[]})
						if not self.sidebar_first:
							if (self.has_sidebar()): 
								self.sidebar.build()
								self.layout_list.append({"sidebar":[]})
					if(self.has_footer()):
						self._footer.build()
						self.layout_list.append({"footer":[]})
				# Layout 5 depends on the CSS RULE!
			else:
				print("No sidebar")
				print(make_menu_header)
				make_menu_header()
				self.layout_list.append({"menu":[]})
				div(cls="container-fluid py-3", id="page-content")
				self.layout_list.append({"content":[]})
				if has_footer:
					make_footer(random.randint(sizes_limits["footer"][0],sizes_limits["footer"][1]), "credits")
					self.layout_list.append({"footer":[]})
			
			# self.add_header_navbar()
			# self.add(self.sidebar)
			#self.main_doc = doc

	def build_header_navbar(self):
		if self.navbar_first:
			if (self.has_navbar()):
				self.navbar.build()
				self.layout_list.append({"navbar":[]})
		if self.has_header():
			self._header.build()
			self.layout_list.append({"header":[]})
		if not self.navbar_first:
			if (self.has_navbar()):
				self.navbar.build()
				self.layout_list.append({"navbar":[]})
	
	def add(self, *args):
		'''
		Adding tags to a a weblayout that build the content where it's called if it
		the elements aren't None.
		'''
		not_none_args = []
		for arg in args:
			if arg is not None:
				not_none_args.append(arg)
		return self._entry.add(*not_none_args)

	def save(self, output_path="./output/"):
		result = open(output_path+"rw.html","w+")
		result.write(self.render())
		result.close()

	def has_footer(self):
		return not isinstance(self._footer, EmptyHtmlComponent)

	def has_header(self):
		return not isinstance(self._header, EmptyHtmlComponent)

	def has_navbar(self):
		return not isinstance(self.navbar, EmptyHtmlComponent)

	def has_sidebar(self):
		return not isinstance(self.sidebar, EmptyHtmlComponent)