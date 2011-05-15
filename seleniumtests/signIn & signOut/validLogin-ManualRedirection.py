from selenium import selenium
import unittest, time, re

class Valid Login - townes.wang [Manual Redirection](unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_valid _login - townes.wang [_manual _redirection](self):
        sel = self.selenium
        sel.open("/signOut")
        sel.open("/")
        sel.click("username")
        sel.type("username", "townes.wang")
        sel.type("password", "test")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Welcome, Townes Wang"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("UPLOAD"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Latest Uploads"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failIf(sel.is_element_present("//form[@action='/signIn/']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Sign Out']")
        sel.wait_for_page_to_load("30000")
        sel.click("link=If you do not wish to wait, please click here to return to the home page.")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Latest Uploads"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        self.assertEqual("", sel.get_text("username"))
        self.assertEqual("", sel.get_text("password"))
        try: self.failUnless(sel.is_element_present("//form[@action='/signIn/']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
