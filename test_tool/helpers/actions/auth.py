from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from test_tool.settings import ADMIN_LOGIN, ADMIN_PASS, DEBUG, USER_LOGIN, USER_PASS
from test_tool.helpers.selenium_stuff import wait_for_one_of_elements
from test_tool.helpers.actions.exceptions import ActionHelperException


def fill_login_form(browser, username=ADMIN_LOGIN, password=ADMIN_PASS):
    browser.find_element_by_id("omniboxLoginEmail").send_keys(username)
    browser.find_element_by_id("omniboxLoginPassword").send_keys(password)
    browser.find_element_by_css_selector('button[type="submit"]').click()


def log_in_if_necessary(browser, username=ADMIN_LOGIN, password=ADMIN_PASS):
    result = wait_for_one_of_elements({
                "login_form": (browser.find_element_by_id, ('omniboxLoginEmail')),
                "already_logged_in": (browser.find_elements_by_css_selector, ('a[href="/dashboard"]')),
    }, only_visible=True)
    if DEBUG:
        print result[0]

    if result[0] == "login_form":
        fill_login_form(browser, username=username, password=password)
    else:
        return

    result = wait_for_one_of_elements({
            "login_failed_popup": (browser.find_element_by_css_selector, ('#omniboxMessage.error')),
            "logged_in": (browser.find_elements_by_css_selector, ('a[href="/dashboard"]')),
    }, only_visible=True)
    if DEBUG:
        print result[0]

    if result[0] in ["login_failed_popup", ]:
        raise ActionHelperException("Login failed with '{username}'/'{password}' credentials."
                                    .format(username=username, password=password))


def log_in_as_user_if_necessary(browser, username=USER_LOGIN, password=USER_PASS):
    return log_in_if_necessary(browser, username, password)
