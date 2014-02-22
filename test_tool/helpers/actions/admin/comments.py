from test_tool.settings import DEFAULT_WAIT, LONG_AJAX
from test_tool.helpers.selenium_stuff import(
    scroll_to, hover, wait_for_visible_by_css)


def get_list_of_comments(browser):
    wait_for_visible_by_css(browser, LONG_AJAX, 'tbody tr#use-hover')
    comments_elements = browser.find_elements_by_css_selector(
        'tbody tr#use-hover')
    comments = []
    for element in comments_elements:
        comments.append({
            'element': element,
            'subject': element.find_element_by_css_selector(
                'span.commentSubject').text,
            'content': element.find_element_by_css_selector(
                'p.commentBody').text,
        })
    return comments


def find_comment_element_on_backend(browser, comment_text):
    comments = get_list_of_comments(browser)
    comment_element = [
        comment['element'] for comment in comments
        if comment['content'] == comment_text
    ][0]
    return comment_element


def recommend_comment(browser, comment_element):
    scroll_to(comment_element)
    hover(browser, comment_element)
    recommend_button = wait_for_visible_by_css(
        browser, DEFAULT_WAIT, 'a.action-recommend')
    recommend_button.click()
    wait_for_visible_by_css(browser, LONG_AJAX, 'div.flash')


def make_comment_good(browser, comment_element):
    scroll_to(comment_element)
    hover(browser, comment_element)
    list_select = wait_for_visible_by_css(
        browser, DEFAULT_WAIT, 'ul.select2-choices')
    list_select.click()
    good_choice = wait_for_visible_by_css(
        comment_element, DEFAULT_WAIT,
        'ul.select2-results div.select2-result-label')
    good_choice.click()
    wait_for_visible_by_css(browser, LONG_AJAX, 'div.flash')
