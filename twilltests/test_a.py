import unittest
from twill import get_browser
from twill.commands import *
import os
from shutil import copy

class TestRegis(unittest.TestCase):
    	def setUp(self):
    		self.pgdev = "http://localhost:8000"
    		self.pgdep = "http://savegame.eudisduran.com"
    		#1 if dev, 0 if dep. Change this alone to test elsewhere
    		self.cur = 1 
    		if (self.cur):
    			copy("../project/savegame.db", "../project/savegame.db.copy")
        	self.b = get_browser()  

    	def test_web_page_up(self):
        	pass
		#self.b.go('http://localhost:8000')
        	#html = self.b.result.get_page()
        	#assert(html.find('html')>0)    

	def test_form_on_page_up(self):
        	pass
		#self.b.go('http://localhost:8080')
        	#html = self.b.result.get_page()
        	#assert(html.find('form')>0)    
	
	def tearDown(self):
		if (self.cur):
			os.remove("../project/savegame.db")
			os.rename("../project/savegame.db.copy", "../project/savegame.db")
			

