from unittest import TestCase
from selenium.webdriver.support.ui import Select, WebDriverWait

from test_tool.settings import LONG_AJAX
from test_tool.helpers.selenium_stuff import navigate, id_generator, wait_for_visible
from test_tool.helpers.actions.auth import log_in_as_user_if_necessary
from test_tool.logger import logger

from tests import test_data


class ProfileTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        #if 'foobar' not in SERVER_URL:
        #    raise SkipTest("new advertisement functionality enabled only on 'devel' branch")
        cls.session = test_data.session
        cls.browser_admin = test_data.browser_admin
        cls.browser = test_data.browser_embed
        print('*Article')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_new_article(self):
        """
        Make a new article and check on front-end as editor author articles.
        """
        article_title = id_generator()
        article_content = ' '.join([id_generator() for i in range(20)]) # 20 random "words"

        #first page
        #{{{
        self.browser_admin.get(navigate('/admin/articles/add_move.php'))

        self.browser_admin.find_element_by_css_selector('input[name="f_article_name"]').send_keys(article_title)
        Select(self.browser_admin.find_element_by_css_selector('select[name="f_article_type"]'))\
            .select_by_visible_text('news')
        Select(self.browser_admin.find_element_by_css_selector('select[name="f_article_language"]'))\
            .select_by_visible_text('Deutsch')
        Select(self.browser_admin.find_element_by_css_selector('select[name="f_destination_publication_id"]'))\
            .select_by_visible_text('Tageswoche')

        destination_issue_select = Select(
            wait_for_visible(self.browser_admin, LONG_AJAX,
                lambda br: br.find_element_by_css_selector('select[name="f_destination_issue_number"]')
            )
        )
        most_recent_article = str(max(
            [int(o.get_attribute('value')) for o in destination_issue_select.options]
        ))
        destination_issue_select.select_by_value(most_recent_article)

        Select(wait_for_visible(self.browser_admin, LONG_AJAX,
                lambda br: br.find_element_by_css_selector('select[name="f_destination_section_number"]')))\
            .select_by_visible_text('Basel')

        self.browser_admin.find_element_by_css_selector('input[name="save"]').click()
        #}}}

        #second page
        #{{{
        mce_frame = WebDriverWait(self.browser_admin, LONG_AJAX).until(
                lambda br: br.find_element_by_css_selector('.tinyMCEHolder iframe')
        ) # the first iframe
        self.browser_admin.switch_to_frame(mce_frame)
        self.browser_admin.find_element_by_css_selector('body#tinymce').send_keys(article_content)
        self.browser_admin.switch_to_default_content()

        self.browser_admin.find_element_by_css_selector('input[id="save"]').click()
        article_saved_popup = lambda br:\
            True if max(
                [element.text == 'Article saved.' for element
                in br.find_elements_by_css_selector('div.flash')]
            ) else None
        WebDriverWait(self.browser_admin, LONG_AJAX).until(article_saved_popup)
        logger.debug('popup')

        Select(self.browser_admin.find_element_by_css_selector('select[name="f_action_workflow"]'))\
            .select_by_value('Y')
        webcode = self.browser_admin.find_element_by_xpath('/html/body/div[4]/div[3]/div[5]/div[2]/dl/dd[5]').text
        #}}}

        # checking on frontend
        self.browser.get(navigate(webcode))
        result_title = self.browser.find_element_by_css_selector('article h2').text
        self.assertEqual(article_title, result_title,
                         "Article title not matches")
        result_content = self.browser.find_element_by_xpath('//*[@id="article-front"]/div[1]/section/article/p[2]').text
        self.assertEqual(article_content, result_content,
                         "Article content not matches")
