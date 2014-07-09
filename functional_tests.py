from selenium import webdriver
import unittest


class TestBasicDjango(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def test_to_do_in_title(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    unittest.main()
