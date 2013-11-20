from requests import Session
from threading import local

from test_tool.settings import ADMIN_LOGIN, ADMIN_PASS, BLOGGER_LOGIN, BLOGGER_PASS
from test_tool.helpers.actions.auth import log_in_to_admin_backend_if_necessary, log_in_if_necessary
from test_tool.helpers.selenium_stuff import new_webdriver, navigate


test_data = local()


def setUpModule():
    global test_data
    test_data.session = Session()
    test_data.browser_admin = new_webdriver()
    test_data.browser_guest = new_webdriver()
    test_data.browser_blogger = new_webdriver()

    test_data.browser_admin.get(navigate('/auth'))
    log_in_if_necessary(test_data.browser_admin, username=ADMIN_LOGIN, password=ADMIN_PASS)

    test_data.browser_blogger.get(navigate('/admin'))
    log_in_to_admin_backend_if_necessary(test_data.browser_blogger, username=BLOGGER_LOGIN, password=BLOGGER_PASS)


def tearDownModule():
    global test_data
    test_data.browser_admin.close()
    test_data.browser_guest.close()
