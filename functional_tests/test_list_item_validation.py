
from .base import FunctionTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTEst(FunctionTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        pass



