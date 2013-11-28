from test_tool.logger import logger
from test_tool.settings import ADMIN_LOGIN, ADMIN_PASS, USER_MAIL, USER_PASS, ADMIN_MAIL
from test_tool.helpers.selenium_stuff import wait_for_one_of_elements
from test_tool.helpers.actions.exceptions import ActionHelperException


def fill_login_form(browser, email=USER_MAIL, password=USER_PASS):
    browser.find_element_by_id("omniboxLoginEmail").send_keys(email)
    browser.find_element_by_id("omniboxLoginPassword").send_keys(password)
    browser.find_element_by_css_selector('button[type="submit"]').click()


def fill_login_form_mobile(browser, email=USER_MAIL, password=USER_PASS):
    browser.find_element_by_id("omniboxLoginEmailMobile").send_keys(email)
    browser.find_element_by_id("omniboxLoginPasswordMobile").send_keys(password)
    browser.find_element_by_xpath('//*[@id="omniboxLoginFormMobile"]/ul/li[2]/ul/li[4]/button').click()


def fill_login_form_admin(browser, username=ADMIN_LOGIN, password=ADMIN_PASS):
    browser.find_element_by_css_selector('input[name="f_user_name"]').send_keys(username)
    browser.find_element_by_css_selector('input[name="f_password"]').send_keys(password)
    browser.find_element_by_css_selector('input[name="Login"]').click()


def log_in_if_necessary(browser, email=USER_MAIL, password=USER_PASS):
    result = wait_for_one_of_elements({
        "login_form": (browser.find_element_by_id, ('omniboxLoginEmail')),
        "login_form_mobile": (browser.find_element_by_id, ('omniboxLoginEmailMobile')),
        "already_logged_in": (browser.find_elements_by_css_selector, ('a[href="/dashboard"]')),
    }, only_visible=True)
    logger.debug(result[0])

    if result[0] == "login_form":
        fill_login_form(browser, email=email, password=password)
    elif result[0] == "login_form_mobile":
        fill_login_form_mobile(browser, email=email, password=password)
    else:
        return

    result = wait_for_one_of_elements({
        "login_failed_popup": (browser.find_element_by_css_selector, ('#omniboxMessage.error')),
        "logged_in": (browser.find_elements_by_css_selector, ('a[href="/dashboard"]')),
        "logged_in_mobile": (browser.find_elements_by_css_selector, ('li.user-logged')),
    }, only_visible=True)
    logger.debug(result[0])

    if result[0] in ["login_failed_popup", ]:
        raise ActionHelperException("Login failed with '{email}'/'{password}' credentials."
                                    .format(email=email, password=password))
    return result[0]


def log_in_to_admin_backend_if_necessary(browser, username=ADMIN_LOGIN, password=ADMIN_PASS):
    result = wait_for_one_of_elements({
        "login_form": (browser.find_element_by_css_selector, ('input[name="f_user_name"]')),
        "already_logged_in": (browser.find_elements_by_css_selector, ('a[href="/admin/auth/logout"]')),
    }, only_visible=True)
    logger.debug(result[0])

    if result[0] == "login_form":
        fill_login_form_admin(browser, username=username, password=password)
    else:
        return

    result = wait_for_one_of_elements({
        "login_failed": (browser.find_element_by_css_selector, ('div.login_error')),
        "logged_in": (browser.find_elements_by_css_selector, ('a[href="/admin/auth/logout"]')),
    }, only_visible=True)
    logger.debug(result[0])

    if result[0] in ["login_failed", ]:
        raise ActionHelperException("Login failed with '{username}'/'{password}' credentials."
                                    .format(username=username, password=password))
    return result[0]
