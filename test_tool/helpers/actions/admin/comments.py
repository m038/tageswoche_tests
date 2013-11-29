from test_tool.settings import DEFAULT_WAIT, LONG_AJAX
from test_tool.helpers.selenium_stuff import wait_for_visible, scroll_to, hover


def get_list_of_comments(browser):
    wait_for_visible(browser, LONG_AJAX, lambda br: br.find_element_by_css_selector('tbody tbody tr'))
    comments_elements = browser.find_elements_by_css_selector('tbody tr.status_approved')
    comments = []
    for element in comments_elements:
        comments.append({
            'element': element,
            'subject': element.find_element_by_css_selector('td.commentMessage span.commentSubject').text,
            'content': element.find_element_by_css_selector('td.commentMessage p.commentBody').text,
        })
    return comments


def find_comment_element_on_backend(browser, comment_text):
    comments = get_list_of_comments(browser)
    comment_element = [
        comment['element'] for comment in comments
        if comment['content'] == unicode(comment_text)
    ][0]
    return comment_element


def recommend_comment(browser, comment_element):
    scroll_to(comment_element)
    hover(browser, comment_element)
    recommend_button = wait_for_visible(comment_element, DEFAULT_WAIT,
                                        lambda el: el.find_element_by_css_selector('a.action-recommend'))
    recommend_button.click()
    wait_for_visible(browser, LONG_AJAX, lambda br: br.find_element_by_css_selector('div.flash'))
