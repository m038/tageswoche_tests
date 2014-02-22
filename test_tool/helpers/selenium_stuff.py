import os
import string
import random
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException, StaleElementReferenceException)

from test_tool.settings import (
    SERVER_URL, ADMIN_URI, DEFAULT_WAIT, WEBDRIVER, MAX_WAIT, TZ, MOBILE)


class SeleniumHelperException(Exception):
    pass


class NeedReloadException(Exception):
    pass


def new_webdriver(webdriver_name=WEBDRIVER):
    webdriver_name = webdriver_name.lower()
    if webdriver_name == 'firefox':
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.http.phishy-userpass-length', 255)
        driver = webdriver.Firefox(firefox_profile=profile)
        if not MOBILE:
            driver.set_window_size(1024, 768)
        else:
            driver.set_window_size(600, 800)
        return driver
    elif webdriver_name == 'chrome':
        #import pudb; pudb.set_trace()
        return webdriver.Chrome(port=47155)
    else:
        raise SeleniumHelperException(
            "'{0}' webdriver is not defined".format(webdriver_name))


def navigate(uri):
    return urljoin(SERVER_URL, uri)


def navigate_admin(anchor=''):
    return urljoin(navigate(ADMIN_URI), anchor)


def wait_for_one_of_elements(dict_of_functions, only_visible=False,
                             timeout=MAX_WAIT):
    """
    :param dict_of_functions: {
            'function_id': (function, params, should_be_visible(optional)) }
    :return: ('function_id', function_result)
    """
    result_id = None
    result = None
    time_taken = 0
    while not result:

        for function_id, item in dict_of_functions.items():

            try:
                (function, params, should_be_visible) = item
            except ValueError:
                (function, params) = item
                should_be_visible = only_visible

            try:
                result = function(params)
                result_id = function_id
                try:
                    result_is_displayed = result.is_displayed()
                except AttributeError:
                    try:
                        result_is_displayed = max(
                            [r.is_displayed() for r in result])
                    except (IndexError, TypeError, ValueError):
                        result_is_displayed = False
                    except StaleElementReferenceException:
                        pass
                except StaleElementReferenceException:
                    result_is_displayed = False
                if should_be_visible and not result_is_displayed:
                    result_id = None
                    result = None
                if result is not None:
                    break
            except NoSuchElementException:
                pass

        if not result:
            if time_taken >= timeout:
                raise SeleniumHelperException(
                    "Max timeout reached for waiting for element")
            time.sleep(DEFAULT_WAIT)
            time_taken += DEFAULT_WAIT

    return result_id, result


def toogle_checkbox_on(checkbox):
    if not checkbox.is_selected():
        checkbox.click()


def toogle_checkbox_off(checkbox):
    if checkbox.is_selected():
        checkbox.click()


def id_generator(size=20, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for i in range(size))


def get_image_name_from_path(path):
    image_name, null = os.path.splitext(path.split('/')[-1])
    return image_name


def find_element_by_text(browser, text):
    return browser.find_element_by_xpath(
        "//*[contains(text(), '{text}')]".format(text=text))


def find_elements_by_text(browser, text):
    return browser.find_elements_by_xpath(
        "//*[contains(text(), '{text}')]".format(text=text))


def parent(element):
    return element.find_element_by_xpath('..')


def wait_for_visible(obj, timeout, function, until_not=False):
    start_time = int(time.time())
    time_elapsed = 0
    elem = None
    while time_elapsed < timeout:
        try:
            elem = function(obj)
        except NoSuchElementException:
            if until_not:
                return
        if elem is not None:
            try:
                if elem.is_displayed() != until_not:
                    return elem
            except StaleElementReferenceException:
                pass
        time_elapsed = int(time.time()) - start_time
        time.sleep(DEFAULT_WAIT)
    raise SeleniumHelperException("Max timeout reached for waiting for\
 visible element.")


def wait_for_visible_by_css(browser, timeout, selector, until_not=False):
    function = lambda br: br.find_element_by_css_selector(selector)
    try:
        return wait_for_visible(browser, timeout, function, until_not)
    except SeleniumHelperException:
        raise SeleniumHelperException(
            "Max timeout reached for waiting for visible element '{0}'."
            .format(selector)
        )


def wait_for_visible_by_id(browser, timeout, selector, until_not=False):
    function = lambda br: br.find_element_by_id(selector)
    try:
        return wait_for_visible(browser, timeout, function, until_not)
    except SeleniumHelperException:
        raise SeleniumHelperException(
            "Max timeout reached for waiting for visible element '#{0}'."
            .format(selector)
        )


def wait_for_visible_text_by_css(browser, timeout, selector, text,
                                 case_sensitive=False, partial=False,
                                 until_not=False, wrong_text=False):
    def function(br):
        elements = br.find_elements_by_css_selector(selector)
        for element in elements:
            if case_sensitive:
                element_text = element.text
                right_text = text
            else:
                element_text = element.text.lower()
                right_text = text.lower()
            if (
                    (right_text == element_text and not partial) or
                    (right_text in element_text and partial) or
                    (wrong_text and
                     (right_text != element_text and not partial) or
                     (right_text not in element_text and partial)
                    )):
                return element
        return None
    try:
        return wait_for_visible(browser, timeout, function, until_not)
    except SeleniumHelperException:
        raise SeleniumHelperException(
            "Max timeout reached for waiting for visible element '{0}' with \
                text '{1}'.".format(selector, text)
        )


def hover(browser, element):
    action = ActionChains(browser).move_to_element(element)
    action.perform()


def scroll_to(element):
    return element.location_once_scrolled_into_view


def drag(browser, element_from, element_to):
    ActionChains(browser).drag_and_drop(element_from, element_to).perform()


def alt_click(browser, element):
    """
    i love our javascript coders...
    """
    action = ActionChains(browser).click_and_hold(element)
    action.perform()
    time.sleep(DEFAULT_WAIT)
    action = ActionChains(browser).release(element)
    action.perform()


def unescape(s):
    return s.replace('&amp;', '&')


def accept_js_alert(browser):
    alert = browser.switch_to_alert()
    msg = alert.text  # it's workaround for 'a is null'
    alert.accept()
    return msg


def dismiss_js_alert(browser):
    alert = browser.switch_to_alert()
    msg = alert.text  # it's workaround for 'a is null'
    alert.dismiss()
    return msg


def get_true_text(element):
    children = element.find_elements_by_xpath('*')
    original_text = element.text
    for child in children:
        original_text = original_text.replace(child.text, '', 1)
    return original_text


def get_or_refresh(browser, uri):
    url = navigate(uri)
    if browser.current_url == url:
        browser.refresh()
    else:
        browser.get(url)


def get_current_time():
    offset = TZ if time.localtime().tm_isdst == 0 else TZ + 1
    return datetime.utcnow() + timedelta(hours=offset)
