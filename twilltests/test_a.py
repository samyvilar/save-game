import unittest
from twill import get_browser
from twill.commands import *
import os
from shutil import copy

class TestASar(unittest.TestCase):
    def setUp(self):
        #True if dev, False if dep. Change this alone to test on the other page
        self.cur = True 
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
        
    def test_registration(self):
        ul = ["test_reg_user1", "test_reg_user2", "test_reg_user3"]
        p = "abc123"
        em = "noreplysavegame@gmail.com"
        for i in range(len(ul)):
            self.b.go(self.pg+"/registration")
            fv (3, "username", ul[i])
            fv (3, "password", p)
            fv (3, "repassword", p)
            fv (3, "email", em)
            submit()
            sleep()
            reset_browser()
            self.b = get_browser()
            self.b.go(self.pg)
            fv (2, "username", ul[i])
            fv (2, "password", p)
            submit()
            sleep()            
            html = self.b.result.get_page()
            assert(html.find("Invalid Username or Password: Please check your credentials.") == -1)
        
    def test_search(self):
        sl = ["portal", "port", "akshai", "cry"]
        rl = ["Portal 2", "Portal 2", "World of Warcraft", "Crysis 2"]
        for i in range(len(sl)):
            self.b.go(self.pg)
            fv("search_form", "search", sl[i])
            submit()
            sleep()
            html = self.b.result.get_page()
            assert(html.find(rl[i]) > 0)
	
    def tearDown(self):
        if (self.cur):
            os.remove("../project/savegame.db")
            os.rename("../project/savegame.db.copy", "../project/savegame.db")
			

