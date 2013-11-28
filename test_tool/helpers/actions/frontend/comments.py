from selenium.webdriver.support.ui import WebDriverWait

from test_tool.settings import MAX_WAIT
from test_tool.helpers.selenium_stuff import id_generator, wait_for_visible


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
