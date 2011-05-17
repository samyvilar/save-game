from selenium import selenium
import unittest, time, re

class Invalid Login(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_invalid _login(self):
        sel = self.selenium
        sel.open("/signOut")
        sel.open("/")
        sel.click("username")
        sel.type("username", "invalidLogin")
        sel.type("password", "invalidPassword")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Invalid Username or Password: Please check your credentials."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@id='signInForm']/fieldset[1]/legend"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("//form[@action='/signIn/']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failIf(sel.is_text_present("UPLOAD"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
