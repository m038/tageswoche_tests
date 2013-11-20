from requests import Session
import threading

from test_tool.settings import ADMIN_LOGIN, ADMIN_PASS, BLOGGER_LOGIN, BLOGGER_PASS
from test_tool.helpers.actions.auth import log_in_to_admin_backend_if_necessary, log_in_if_necessary
from test_tool.helpers.selenium_stuff import new_webdriver, navigate


test_data = threading.local()


def setUpModule():
    global test_data
    test_data.session = Session()
    test_data.browser_admin = new_webdriver()
    test_data.browser_guest = new_webdriver()
    test_data.browser_blogger = new_webdriver()

    browser_admin = test_data.browser_admin
    browser_blogger = test_data.browser_blogger

    def log_in_admin():
        browser_admin.get(navigate('/admin'))
        log_in_to_admin_backend_if_necessary(browser_admin, username=ADMIN_LOGIN, password=ADMIN_PASS)

    def log_in_blogger():
        browser_blogger.get(navigate('/admin'))
        log_in_to_admin_backend_if_necessary(browser_blogger, username=BLOGGER_LOGIN, password=BLOGGER_PASS)

    thread2 = threading.Thread(target=log_in_blogger)
    thread2.start()
    thread1 = threading.Thread(target=log_in_admin)
    thread1.start()
    while threading.active_count() >1:
        pass


def tearDownModule():
    global test_data
    test_data.browser_admin.close()
    test_data.browser_guest.close()
    test_data.browser_blogger.close()
