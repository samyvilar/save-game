import unittest
from twill import get_browser
from twill.commands import *
import os
from shutil import copy

class Test_AS(unittest.TestCase):
    def setUp(self):
        #True if dev, False if dep. Change this alone to test on the other page
        #If on dep, need to go to django admin and delete test_reg_user1,2,3 after
        self.cur = True 
        if (self.cur):
            self.pg = "http://localhost:8000"
            copy("../project/savegame.db", "../project/savegame.db.copy")
        else:
            self.pg = "http://savegame.eudisduran.com"
        self.b = get_browser()  

    def test_web_page_up(self):
        self.b.go(self.pg)
        assert(self.b.result.get_page().find('html')>0)    

    def test_form_on_page_up(self):
        self.b.go(self.pg)
        assert(self.b.result.get_page().find('form')>0)
        
    def test_latest_uploads(self):
        self.b.go(self.pg)
        assert(self.b.result.get_page().find('Nothing was uploaded so far') == -1   )
        
    def test_registration(self):
        ul = ["test_reg_user1", "test_reg_user2", "test_reg_user3"]
        p = "abc123"
        em = "noreplysavegame@gmail.com"
        for i in range(len(ul)):
            self.b.go(self.pg+"/registration")
            fv ("registration_form", "username", ul[i])
            fv ("registration_form", "password", p)
            fv ("registration_form", "repassword", p)
            fv ("registration_form", "email", em)
            submit()
            sleep()
            reset_browser()
            self.b = get_browser()
            self.b.go(self.pg)
            fv (2, "username", ul[i])
            fv (2, "password", p)
            submit()
            sleep()            
            assert(self.b.result.get_page().find("Invalid Username or Password: Please check your credentials.") == -1)
    
    def test_registration_fails(self):
        self.b.go(self.pg+"/registration")
        fv ("registration_form", "username", "akshai.sarma")
        fv ("registration_form", "password", "pass")
        fv ("registration_form", "repassword", "diffpass")
        fv ("registration_form", "email", "pass.com") 
        submit()
        sleep()
        res = self.b.result.get_page()
        assert(res.find("That username already exists!") > 0)
        assert(res.find("The passwords do not match!") > 0)
        assert(res.find("Enter a valid e-mail address") > 0)
        
    def test_search(self):
        sl = ["portal", "port", "akshai", "cry"]
        rl = ["Portal 2", "Portal 2", "World of Warcraft", "Crysis 2"]
        for i in range(len(sl)):
            self.b.go(self.pg)
            fv("search_form", "search", sl[i])
            submit()
            sleep()
            assert(self.b.result.get_page().find(rl[i]) > 0)    
	
    def tearDown(self):
        if (self.cur):
            os.remove("../project/savegame.db")
            os.rename("../project/savegame.db.copy", "../project/savegame.db")
			

