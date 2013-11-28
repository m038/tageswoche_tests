import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.settings import MAX_WAIT, LONG_AJAX
from test_tool.helpers.selenium_stuff import id_generator, wait_for_visible, get_true_text


def add_comment(browser, subject=None, content=None):
    if subject is None:
        subject = id_generator()
    if content is None:
        content = id_generator()
    comment_button = WebDriverWait(browser, MAX_WAIT).until(
        lambda br: br.find_element_by_css_selector('#comments > a.button')
    )
    comment_button.click()
    subject_field = wait_for_visible(browser, MAX_WAIT,
                                     lambda br: br.find_element_by_id('omniboxCommentSubject'))
    subject_field.send_keys(subject)
    content_field = browser.find_element_by_id('omniboxCommentContent')
    content_field.send_keys(content)
    send_button = browser.find_element_by_css_selector('#omniboxCommentForm button[type="submit"]')
    send_button.click()
    wait_for_visible(browser, MAX_WAIT,
                     lambda br: br.find_element_by_id('omniboxComment'),
                     until_not=True)
    return {
        'subject': subject,
        'content': content
    }


def get_all_comments_elements(browser):

    def waiting_function(br):
        try:
            show_more_link = browser.find_element_by_css_selector('#weitere_kommentare a')
            if show_more_link.is_displayed():
                show_more_link.click()
        except NoSuchElementException:
            pass
        elements = br.find_elements_by_css_selector('#alle-kommentare li')
        return elements if len(elements) == comments_number else None

    all_comments_button = WebDriverWait(browser, MAX_WAIT).until(
        lambda br: br.find_element_by_css_selector('a[href="#alle-kommentare"]')
    )
    all_comments_button.click()
    pattern = re.compile('\d+')
    comments_number = int(pattern.findall(all_comments_button.text)[0])
    comments_elements = WebDriverWait(browser, LONG_AJAX).until(waiting_function)
    return comments_elements


def get_all_comments_contents(browser):
    comments_elements = get_all_comments_elements(browser)
    comments = {}
    pattern = re.compile('(.*)\n$')
    for element in comments_elements:
        comment_id = element.get_attribute('data-comment-id')
        comments[comment_id] = {
            'subject': element.find_element_by_css_selector('h4').text,
            'content': pattern.findall(get_true_text(element.find_element_by_css_selector('p')))[0],
            #'author': element.find_element_by_css_selector('span.comment-uname').text,
            'author': element.find_element_by_xpath('//small/a').text,
        }
    return comments
