from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.settings import MAX_WAIT


class AdditionalVerifiesTestClass(object):

    def verify_selector(self, selector):
        try:
            return WebDriverWait(self.browser, MAX_WAIT).until(
                lambda br: br.find_element_by_css_selector(selector)
            )
        except TimeoutException:
            self.fail("No {selector}".format(selector=selector))

    def verify_text_in_selector(self, selector, text):
        try:
            WebDriverWait(self.browser, MAX_WAIT).until(
                lambda br: True if text in
                br.find_element_by_css_selector(selector).text
                else None
            )
        except TimeoutException:
            print(self.browser.find_element_by_css_selector(selector).text)
            self.fail(u"'{text}' is not in '{selector}'".format(text=text, selector=selector))

    def verify_text_in_selectors_attribute(self, selector, attribute, text):
        try:
            WebDriverWait(self.browser, MAX_WAIT).until(
                lambda br: True if text in
                br.find_element_by_css_selector(selector).get_attribute(attribute)
                else None
            )
        except TimeoutException:
            self.fail(u"{text} is not in '{selector}'".format(text=text, selector=selector))

    def verify_number_of_elements(self, selector, number):
        try:
            WebDriverWait(self.browser, MAX_WAIT).until(
                lambda br: True if len(br.find_elements_by_css_selector(selector)) == number
                else None
            )
        except TimeoutException:
            self.fail("No {number} of '{selector}'".format(number=number, selector=selector))
