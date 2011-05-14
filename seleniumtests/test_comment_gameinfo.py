from selenium import selenium
import unittest, time, re

class test_comment_gameinfo(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://localhost:8000/")
        self.selenium.start()
    
    def test_test_comment_gameinfo(self):
        sel = self.selenium
        sel.open("/gamepage/?uploaded_game_id=995")
        sel.click("sub")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
