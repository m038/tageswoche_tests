from test_tool.settings import DEFAULT_WAIT, LONG_AJAX
from test_tool.helpers.selenium_stuff import wait_for_visible


def sort_by_date(browser):
    sort_icon = wait_for_visible(browser, LONG_AJAX, lambda br: br.find_element_by_css_selector(
        '.commentTimeCreated .DataTables_sort_icon')
    )
    while not 'ui-icon-triangle-1-s' in sort_icon.get_attribute('class').split():
        sort_icon.click()


def get_list_of_feedback(browser):
    sort_by_date(browser)
    wait_for_visible(browser, LONG_AJAX, lambda br: br.find_element_by_css_selector(
        'tbody tr td.commentMessage p.commentBody'))
    feedbacks_elements = browser.find_elements_by_css_selector('tbody tr td.commentMessage')
    feedbacks = []
    for element in feedbacks_elements:
        feedbacks.append({
            'subject': element.find_element_by_css_selector('span.commentSubject').text,
            'content': element.find_element_by_css_selector('p.commentBody').text,
        })
    return feedbacks


def find_feedback_element_on_backend(browser, comment_text):
    comments = get_list_of_feedback(browser)
    comment_element = [
        comment['element'] for comment in comments
        if comment['content'] == comment_text
    ][0]
    return comment_element
