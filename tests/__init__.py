from requests import Session
import threading

from test_tool.settings import (
    ADMIN_LOGIN, ADMIN_PASS, BLOGGER_LOGIN, BLOGGER_PASS, USER_MAIL, USER_PASS,
    PRODUCTION)
from test_tool.helpers.actions.auth import (
    log_in_to_admin_backend_if_necessary, log_in_if_necessary)
from test_tool.helpers.selenium_stuff import new_webdriver, navigate


test_data = threading.local()


def setUpModule():
    global test_data
    test_data.session = Session()
    test_data.browser_guest = new_webdriver()
    test_data.browser_user = new_webdriver()

    def log_in_user():
        browser_user.get(navigate('/auth'))
        log_in_if_necessary(browser_user, email=USER_MAIL, password=USER_PASS)

    def log_in_admin():
        browser_admin.get(navigate('/admin'))
        log_in_to_admin_backend_if_necessary(
            browser_admin, username=ADMIN_LOGIN, password=ADMIN_PASS)

    def log_in_blogger():
        browser_blogger.get(navigate('/admin'))
        log_in_to_admin_backend_if_necessary(
            browser_blogger, username=BLOGGER_LOGIN, password=BLOGGER_PASS)

    def open_guest():
        browser_guest.get(navigate('/'))

    browser_user = test_data.browser_user
    thread_user = threading.Thread(target=log_in_user)
    thread_user.start()
    browser_guest = test_data.browser_guest
    thread_guest = threading.Thread(target=open_guest)
    thread_guest.start()

    if not PRODUCTION:
        test_data.browser_admin = new_webdriver()
        test_data.browser_blogger = new_webdriver()
        browser_admin = test_data.browser_admin
        browser_blogger = test_data.browser_blogger
        thread_admin = threading.Thread(target=log_in_admin)
        thread_admin.start()
        thread_blogger = threading.Thread(target=log_in_blogger)
        thread_blogger.start()

    while threading.active_count() > 1:
        pass


def tearDownModule():
    global test_data
    test_data.browser_guest.close()
    test_data.browser_user.close()
    if not PRODUCTION:
        test_data.browser_admin.close()
        test_data.browser_blogger.close()
