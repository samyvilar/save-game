from selenium import selenium
import unittest

ffpath = "/Applications/Firefox 3.6.17.app/Contents/MacOS/firefox-bin"
class voting(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox3 " + ffpath, "http://localhost:8000/")
        self.selenium.start()
    
    def test_voting(self):
        sel = self.selenium
        sel.open("/")
        sel.click("username")
        sel.type("username", "akshai.sarma")
        sel.click("password")
        sel.type("password", "sarma")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        sel.open("/gamepage/?uploaded_game_id=995")
        uv = sel.get_text("upvotes")
        dv = sel.get_text("downvotes")
        sel.click("upv")
        sel.click("upv")
        sel.click("dnv")
        sel.click("dnv")
        try: self.assertEqual(uv, sel.get_text("upvotes"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual(dv, sel.get_text("downvotes"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Sign Out']")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)
