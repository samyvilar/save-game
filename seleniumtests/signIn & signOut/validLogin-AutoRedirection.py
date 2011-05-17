from selenium import selenium
import unittest, time, re

class Valid Login - twang [Automatic Redirection](unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_valid _login - twang [_automatic _redirection](self):
        sel = self.selenium
        sel.open("/signOut")
        sel.open("/")
        sel.click("username")
        sel.type("username", "twang")
        sel.type("password", "twang")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Welcome, twang"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("UPLOAD"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failIf(sel.is_element_present("//form[@action='/signIn/']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//input[@value='Sign Out']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("You have been successfully signed out . You will be automatically redirected to the home page in 10 seconds."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if "Latest Uploads" == sel.get_text("//div[@id='latestTitle']/h2"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
