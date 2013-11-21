from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import navigate, id_generator
from test_tool.helpers.actions.article import create_new_article, publish_article, create_new_blog
from test_tool.settings import PRODUCTION

from tests import test_data


class ProfileTestCase(TestCase):

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
            article_title=self.article_title,
            article_type='news',
            article_language='Deutsch',
            article_publication='Tageswoche',
            article_section='Basel'
        )
        self.edit_url = self.browser_admin.current_url
        self.webcode = publish_article(self.browser_admin, self.article_content)

    def tearDown(self):
        pass

    def test_add_new_article(self):
        """
        Create a new article and check it on front-end.
        """
        self.browser.get(navigate(self.webcode))
        result_title = self.browser.find_element_by_css_selector('article h2').text
        self.assertEqual(self.article_title, result_title,
                         "Article title not matches")
        result_content = self.browser.find_element_by_xpath('//*[@id="article-front"]/div[1]/section/article/p[2]').text
        self.assertEqual(self.article_content, result_content,
                         "Article content not matches")
