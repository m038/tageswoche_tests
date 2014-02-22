from selenium.webdriver.support.ui import WebDriverWait

from test_tool.settings import MAX_WAIT, DEFAULT_WAIT
from test_tool.helpers.selenium_stuff import (
    id_generator, wait_for_visible, wait_for_visible_by_css)


def add_feedback(browser, subject=None, content=None):
    if subject is None:
        subject = id_generator()
    if content is None:
        content = id_generator()
    feedback_button = WebDriverWait(browser, MAX_WAIT).until(
        lambda br: br.find_element_by_css_selector('#omnibox a.trigger')
    )
    feedback_button.click()

    try:
        feedback_option = wait_for_visible_by_css(
            browser, DEFAULT_WAIT,
            "#omniboxCommentRadioFeedback")
    except:
        pass
    else:
        feedback_option.click()

    subject_field = wait_for_visible_by_css(
        browser, MAX_WAIT, 'omniboxFeedbackSubject')
    subject_field.send_keys(subject)
    content_field = browser.find_element_by_id('omniboxFeedbackContent')
    content_field.send_keys(content)
    send_button = wait_for_visible_by_css(
        browser, MAX_WAIT, '#omniboxFeedbackForm button[type="submit"]')
    send_button.click()
    hide_omni = wait_for_visible_by_css(
        browser, MAX_WAIT, '#omniboxMessage a')
    hide_omni.click()
    return {
        'subject': subject,
        'content': content
    }
