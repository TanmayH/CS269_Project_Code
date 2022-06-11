from __future__ import absolute_import
from Sampler import *

sampler = Sampler()
with open("test.gui","r") as f:
    gui_string = f.read()
    print(gui_string)
