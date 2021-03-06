from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerCase
from django.utils.html import escape
from lists.forms import EMPTY_LIST_ERROR


class FunctionalTest(StaticLiveServerCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, 'lists/.+')

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')
        self.browser.quit()
        #a new user comes along; fracis shouldn't see edith's list
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_text')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertContains(response, escape(EMPTY_LIST_ERROR))

        self.browser.find_element_by_id('id_text').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        self.browser.find_element_by_id('id_text').send_keys('\n')

        self.check_for_row_in_list_table('1: Buy milk')
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

        self.browser.find_element_by_id('id_text').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies\n')

        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")
        self.assertFalse(error.is_displayed())
