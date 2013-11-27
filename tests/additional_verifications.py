from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.settings import MAX_WAIT


class AdditionalVerifiesTestClass(object):

    def verify_selector(self, selector):
        def verify_function(br):
            result = br.find_element_by_css_selector(selector)
            if result.is_displayed():
                return result
            else:
                return None
        try:
            return WebDriverWait(self.browser, MAX_WAIT).until(verify_function)
        except TimeoutException:
            self.fail("No '{selector}' on page.".format(selector=selector))

    def verify_text_in_selector(self, selector, text):
        def verify_function(br):
            result = br.find_element_by_css_selector(selector)
            if result.is_displayed() and text in result.text:
                return result
            else:
                return None
        try:
            return WebDriverWait(self.browser, MAX_WAIT).until(verify_function)
        except TimeoutException:
            self.fail(u"'{text}' is not in '{selector}'".format(text=text, selector=selector))

    def verify_text_in_selectors_attribute(self, selector, attribute, text):
        def verify_function(br):
            result = br.find_element_by_css_selector(selector)
            if result.is_displayed() and text in result.get_attribute(attribute):
                return result
            else:
                return None
        try:
            WebDriverWait(self.browser, MAX_WAIT).until(verify_function)
        except TimeoutException:
            self.fail(u"{text} is not in '{selector}'".format(text=text, selector=selector))

    def verify_number_of_elements(self, selector, number):
        def verify_function(br):
            results = br.find_elements_by_css_selector(selector)
            visible_results = [result for result in results if result.is_displayed()]
            if len(visible_results) == number:
                return visible_results
            else:
                return None
        try:
            WebDriverWait(self.browser, MAX_WAIT).until(verify_function)
        except TimeoutException:
            self.fail("No {number} of '{selector}'".format(number=number, selector=selector))
