from selenium import selenium
import unittest, time, re

class mustBeLoggedInToUpload(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_must_be_logged_in_to_upload(self):
        sel = self.selenium
        sel.open("/signOut/")
        sel.click("link=If you do not wish to wait, please click here to return to the home page.")
        sel.wait_for_page_to_load("30000")
        try: self.failIf(sel.is_element_present("UPLOAD"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.open("/upload/")
        try: self.failUnless(sel.is_text_present("You must be logged in to see this page."))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
