from requests import Session
from threading import local

from test_tool.helpers.actions.auth import log_in_to_admin_backend_if_necessary, log_in_if_necessary
from test_tool.helpers.selenium_stuff import new_webdriver, navigate


test_data = local()


def setUpModule():
    global test_data
    test_data.session = Session()
    test_data.browser_admin = new_webdriver()
    test_data.browser_embed = new_webdriver()

    test_data.browser_admin.get(navigate('/auth'))
    log_in_if_necessary(test_data.browser_admin)


def tearDownModule():
    global test_data
    test_data.browser_admin.close()
    test_data.browser_embed.close()
