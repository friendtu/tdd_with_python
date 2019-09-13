from selenium import webdriver
#import unittest
import time
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT=10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError,WebDriverException)as e:
                #StaleElementReferenceException
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)



    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])



    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(10)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

#       self.fail("Finish the test")


    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')

        self.browsr.quit()
        self.browser=webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn（Buy peacok feathers',page_text)
        self.assertNoIn('make a fly',page_text)


#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
