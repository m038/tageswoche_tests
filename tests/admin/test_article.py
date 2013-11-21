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
            raise SkipTest("this tests shouldn't be runned on production")
        cls.session = test_data.session
        cls.browser_admin = test_data.browser_admin
        cls.browser_blogger = test_data.browser_blogger
        cls.browser = test_data.browser_guest

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_new_article(self):
        """
        Create a new article and check it on front-end.
        """
        article_title = id_generator()
        article_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        create_new_article(
            browser=self.browser_admin,
            article_title=article_title,
            article_type='news',
            article_language='Deutsch',
            article_publication='Tageswoche',
            article_section='Basel'
        )
        webcode = publish_article(self.browser_admin, article_content)

        self.browser.get(navigate(webcode))
        result_title = self.browser.find_element_by_css_selector('article h2').text
        self.assertEqual(article_title, result_title,
                         "Article title not matches")
        result_content = self.browser.find_element_by_xpath('//*[@id="article-front"]/div[1]/section/article/p[2]').text
        self.assertEqual(article_content, result_content,
                         "Article content not matches")

    def test_add_blog_record(self):
        """
        Create a new blog record and check it on front-end.
        """
        blog_title = id_generator()
        blog_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        create_new_blog(self.browser_blogger, blog_title)
        webcode = publish_article(self.browser_blogger, blog_content)

        self.browser.get(navigate(webcode))
        result_title = self.browser.find_element_by_xpath('//*[@id="wrapper"]/div[4]/section/article[2]/h2').text
        self.assertEqual(blog_title, result_title,
                         "Blog record title not matches")
        result_content = self.browser.find_element_by_xpath('//*[@id="wrapper"]/div[4]/section/article[2]/p').text
        self.assertEqual(blog_content, result_content,
                         "Blog record content not matches")
