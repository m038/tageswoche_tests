from selenium.webdriver.support.ui import Select, WebDriverWait

from test_tool.settings import LONG_AJAX
from test_tool.helpers.selenium_stuff import navigate, wait_for_visible
from test_tool.helpers.actions.frontend.common import get_current_publication
from test_tool.logger import logger


def create_new_article(browser, browser_frontend, article_title, article_type, article_language, article_publication, article_section):
    browser.get(navigate('/admin/articles/add_move.php'))

    browser.find_element_by_css_selector('input[name="f_article_name"]').send_keys(article_title)
    Select(browser.find_element_by_css_selector('select[name="f_article_type"]'))\
        .select_by_visible_text(article_type)
    Select(browser.find_element_by_css_selector('select[name="f_article_language"]'))\
        .select_by_visible_text(article_language)
    #Select(browser.find_element_by_css_selector('select[name="f_destination_publication_id"]'))\
    #    .select_by_visible_text(article_publication)

    destination_issue_select = Select(
        wait_for_visible(
            browser, LONG_AJAX,
            lambda br: br.find_element_by_css_selector(
                'select[name="f_destination_issue_number"]')
        )
    )
    destination_issue_select.select_by_visible_text(get_current_publication(
        browser_frontend))

    Select(wait_for_visible(browser, LONG_AJAX,
                            lambda br: br.find_element_by_css_selector('select[name="f_destination_section_number"]')))\
        .select_by_visible_text(article_section)

    browser.find_element_by_css_selector('input[name="save"]').click()


def edit_article(browser, article_content, action='save'):
    """
    action: save, close, save_and_close
    """
    try:
        mce_frame = WebDriverWait(browser, 60).until(  # @TODO: hardcoded timeout, and it's too large
            lambda br: br.find_element_by_css_selector('.tinyMCEHolder iframe')
        )  # the first mce iframe
    except Exception as e:
        browser.save_screenshot('mce_bug.png')
        raise e
    browser.switch_to_frame(mce_frame)
    edit_field = browser.find_element_by_css_selector('body#tinymce')
    edit_field.clear()
    edit_field.send_keys(article_content)
    browser.switch_to_default_content()

    browser.find_element_by_css_selector('input[id="{action}"]'.format(action=action)).click()

    if action == 'save':
        WebDriverWait(browser, LONG_AJAX).until(
            lambda br:
            True if max(
                [element.text == 'Article saved.' for element
                 in br.find_elements_by_css_selector('div.flash')]
            ) else None
        )
        logger.debug('popup')
    if action == 'save_and_close':
        WebDriverWait(browser, LONG_AJAX).until(
            lambda br: br.find_element_by_css_selector('div.table')
        )


def publish_article(browser, article_content):
    edit_article(browser, article_content, action='save')

    Select(browser.find_element_by_css_selector('select[name="f_action_workflow"]'))\
        .select_by_value('Y')
    webcode = browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[5]/div[2]/dl/dd[5]').text
    return webcode


def create_new_blog(browser, blog_title):
    browser.get(navigate('/admin'))
    WebDriverWait(browser, LONG_AJAX).until(
        lambda br: br.find_element_by_id('title')
    ).send_keys(blog_title)
    browser.find_element_by_id('submit').click()


def publish_blog(browser, article_content):
    edit_article(browser, article_content, action='save')

    Select(browser.find_element_by_css_selector('select[name="f_action_workflow"]'))\
        .select_by_value('Y')
    webcode = browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[4]/div[2]/dl/dd[5]').text
    return webcode
