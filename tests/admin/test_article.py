from unittest import TestCase, SkipTest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.helpers.selenium_stuff import navigate, id_generator, accept_js_alert, dismiss_js_alert
from test_tool.helpers.actions.admin.article import create_new_article, publish_article, edit_article
from test_tool.settings import PRODUCTION, MAX_WAIT

from tests import test_data


class ArticleTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print('*Article')
        if PRODUCTION:
            raise SkipTest("these tests shouldn't be runned on production")
        cls.browser_admin = test_data.browser_admin
        cls.browser = test_data.browser_guest

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """
        Create a new article and check it on front-end.
        It's prerequisite for other tests in this testcase.
        """
        self.article_title = id_generator()
        self.article_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        create_new_article(
            browser=self.browser_admin,
            browser_frontend=self.browser,
            article_title=self.article_title,
            article_type='news',
            article_language='Deutsch',
            article_publication='Tageswoche',
            article_section='Basel'
        )
        self.webcode = publish_article(self.browser_admin, self.article_content)

    def tearDown(self):
        pass

    def verify_article_content_on_frontend(self, new_content):
        self.browser.get(navigate(self.webcode))
        result_title = self.browser.find_element_by_css_selector('article h2').text
        self.assertEqual(self.article_title, result_title,
                         "Article title not matches")
        result_content = self.browser.find_element_by_xpath('//*[@id="article-front"]/div[1]/section/article/p[2]').text
        self.assertEqual(new_content, result_content,
                         "Article content not matches")

    def verify_article_list_presence(self):
        try:
            WebDriverWait(self.browser_admin, MAX_WAIT).until(
                lambda br: True if 'Article List' in
                                   br.find_element_by_css_selector('div.toolbar.clearfix span.article-title').text
                else None
            )
        except TimeoutException:
            self.fail("Article list wasn't opened")

    def test_add_new_article(self):
        """
        Create a new article and check it on front-end.
        """
        self.verify_article_content_on_frontend(self.article_content)

    def test_edit_article_save_all(self):
        """
        Changing articles as editor - Save All
        """
        new_article_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        edit_article(self.browser_admin, new_article_content, action='save')
        self.verify_article_content_on_frontend(new_article_content)

    def _edit_article_close_and_leave(self):
        """
        Changing articles as editor - Close and leave
        """
        self.skipTest("js alert")
        new_article_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        edit_article(self.browser_admin, new_article_content, action='close')
        WebDriverWait(self.browser_admin, MAX_WAIT).until(accept_js_alert)
        self.verify_article_content_on_frontend(self.article_content)
        self.verify_article_list_presence()

    def _edit_article_close_and_stay(self):
        """
        Changing articles as editor - Close and stay
        """
        self.skipTest("js alert")
        new_article_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        edit_article(self.browser_admin, new_article_content, action='close')
        WebDriverWait(self.browser_admin, MAX_WAIT).until(dismiss_js_alert)
        mce_frame = WebDriverWait(self.browser_admin, 60).until(
            lambda br: br.find_element_by_css_selector('.tinyMCEHolder iframe')
        )  # the first mce iframe
        self.verify_article_content_on_frontend(self.article_content)

    def test_edit_article_save_and_close(self):
        """
        Changing articles as editor - Save and close
        """
        new_article_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        edit_article(self.browser_admin, new_article_content, action='save_and_close')
        self.verify_article_content_on_frontend(new_article_content)
        self.verify_article_list_presence()
