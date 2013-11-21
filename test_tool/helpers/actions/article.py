from selenium.webdriver.support.ui import Select, WebDriverWait

from test_tool.settings import LONG_AJAX
from test_tool.helpers.selenium_stuff import navigate, wait_for_visible
from test_tool.logger import logger


def create_new_article(browser, article_title, article_type, article_language, article_publication, article_section):
    browser.get(navigate('/admin/articles/add_move.php'))

    browser.find_element_by_css_selector('input[name="f_article_name"]').send_keys(article_title)
    Select(browser.find_element_by_css_selector('select[name="f_article_type"]'))\
        .select_by_visible_text(article_type)
    Select(browser.find_element_by_css_selector('select[name="f_article_language"]'))\
        .select_by_visible_text(article_language)
    Select(browser.find_element_by_css_selector('select[name="f_destination_publication_id"]'))\
        .select_by_visible_text(article_publication)

    destination_issue_select = Select(
        wait_for_visible(browser, LONG_AJAX,
                         lambda br: br.find_element_by_css_selector('select[name="f_destination_issue_number"]')
                         )
    )
    most_recent_article = str(max(
        [int(o.get_attribute('value')) for o in destination_issue_select.options]
    ))
    destination_issue_select.select_by_value(most_recent_article)

    Select(wait_for_visible(browser, LONG_AJAX,
                            lambda br: br.find_element_by_css_selector('select[name="f_destination_section_number"]')))\
        .select_by_visible_text(article_section)

    browser.find_element_by_css_selector('input[name="save"]').click()


def publish_article(browser, article_content):
    mce_frame = WebDriverWait(browser, LONG_AJAX).until(
        lambda br: br.find_element_by_css_selector('.tinyMCEHolder iframe')
    )  # the first mce iframe
    browser.switch_to_frame(mce_frame)
    browser.find_element_by_css_selector('body#tinymce').send_keys(article_content)
    browser.switch_to_default_content()

    browser.find_element_by_css_selector('input[id="save"]').click()
    article_saved_popup = lambda br:\
        True if max(
            [element.text == 'Article saved.' for element
             in br.find_elements_by_css_selector('div.flash')]
        ) else None
    WebDriverWait(browser, LONG_AJAX).until(article_saved_popup)
    logger.debug('popup')

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
