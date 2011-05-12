import unittest
from twill import get_browser
from twill.commands import *
import os
from shutil import copy

class TestASar(unittest.TestCase):
    def setUp(self):
        #1 if dev, 0 if dep. Change this alone to test on the other page
        self.cur = 1 
        if (self.cur):
            self.pg = "http://localhost:8000"
            copy("../project/savegame.db", "../project/savegame.db.copy")
        else:
            self.pg = "http://savegame.eudisduran.com"
        self.b = get_browser()  

    def test_web_page_up(self):
        self.b.go(self.pg)
        html = self.b.result.get_page()
        assert(html.find('html')>0)    

    def test_form_on_page_up(self):
        self.b.go(self.pg)
        html = self.b.result.get_page()
        assert(html.find('form')>0)    
	
    def tearDown(self):
        if (self.cur):
            os.remove("../project/savegame.db")
            os.rename("../project/savegame.db.copy", "../project/savegame.db")
			

