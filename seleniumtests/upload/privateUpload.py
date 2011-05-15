from selenium import selenium
import unittest, time, re

class privateUpload(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://127.0.0.1:8000/")
        self.selenium.start()
    
    def test_private_upload(self):
        sel = self.selenium
        sel.open("/signOut/")
        sel.click("logo_title")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_element_present("//form[@action='/signIn/']"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("username")
        sel.type("username", "townes.wang")
        sel.type("password", "test")
        sel.click("//input[@value='Login']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("UPLOAD"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("Welcome, Townes Wang"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=UPLOAD")
        sel.wait_for_page_to_load("30000")
        sel.type("id_game", "22038")
        sel.select("id_platform", "label=PC")
        sel.type("id_file", "C:\\Users\\GLaDOS\\Desktop\\test.txt")
        sel.type("id_title", "Private Upload Test")
        sel.type("id_description", "Private Upload Test\n== Description ==")
        sel.click("id_private")
        sel.click("upload_submit")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Your file has been successfully uploaded."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_text_present("You will be redirected back to the upload page in 10 seconds."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//a[contains(text(),'If you do not wish to wait, please click here to return to the\n                    upload page.')]")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
