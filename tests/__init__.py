from requests import Session
from threading import local

from test_tool.helpers.selenium_stuff import new_webdriver


test_data = local()


def setUpModule():
    global test_data
    test_data.session = Session()
    test_data.browser_admin = new_webdriver()
    test_data.browser_embed = new_webdriver()


def tearDownModule():
    global test_data
    test_data.browser_admin.close()
    test_data.browser_embed.close()
