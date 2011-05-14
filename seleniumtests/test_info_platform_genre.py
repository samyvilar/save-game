from selenium import selenium
import unittest

ffpath = "/Applications/Firefox 3.6.17.app/Contents/MacOS/firefox-bin"
class test_info_platform_genre(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox3 " + ffpath, "http://localhost:8000/")
        self.selenium.start()
    
    def test_info_platform_genre(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=ACTION")
        sel.wait_for_page_to_load("30000")
        sel.click("link=100-Yen Gomibako")
        sel.wait_for_page_to_load("30000")
        sel.click("link=PC")
        sel.wait_for_page_to_load("30000")
        sel.click("link=exact:007: The World is not Enough")
        sel.wait_for_page_to_load("30000")
        sel.type("search_text", "portal")
        sel.click("search_button")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Portal 2")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Portal 2 is an accessible, clever"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Sci-Fi First-Person Shooter")
        sel.wait_for_page_to_load("30000")
        sel.click("link=4")
        sel.wait_for_page_to_load("30000")
        sel.click("link=7")
        sel.wait_for_page_to_load("30000")
        sel.click("link=10")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Portal 2", sel.get_text("link=Portal 2"))
        except AssertionError, e: self.verificationErrors.append(str(e))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)
