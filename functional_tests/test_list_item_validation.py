
from .base import FunctionTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionTest):
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.send_key_to_Item_input_box(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        self.send_key_to_Item_input_box("Buy milk")
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.send_key_to_Item_input_box(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        self.send_key_to_Item_input_box(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        self.send_key_to_Item_input_box("Make tea")
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.send_key_to_Item_input_box(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy milk")
        self.wait_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.send_key_to_Item_input_box("Buy wellies")
        self.send_key_to_Item_input_box(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        self.send_key_to_Item_input_box("Buy wellies")
        self.send_key_to_Item_input_box(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleaned_on_input(self):
        self.browser.get(self.live_server_url)
        self.send_key_to_Item_input_box("Benter too thick")
        self.send_key_to_Item_input_box(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Benter too thick")
        self.send_key_to_Item_input_box("Benter too thick")
        self.send_key_to_Item_input_box(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        self.send_key_to_Item_input_box('a')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))




