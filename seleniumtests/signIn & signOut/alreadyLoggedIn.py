from selenium import selenium
import unittest, time, re

class alreadyLoggedIn(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_already_logged_in(self):
        sel = self.selenium
        sel.open("/signOut")
        sel.open("/")
        sel.click("username")
        sel.type("username", "townes.wang")
        sel.type("password", "test")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        sel.open("/signIn")
        try: self.failUnless(sel.is_text_present("You are already signed in."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Sign Out']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=If you do not wish to wait, please click here to return to the home page.")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_element_present("//form[@action='/signIn/']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//div[@id='latestTitle']/h2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
