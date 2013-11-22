from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import navigate, id_generator
from test_tool.helpers.actions.article import create_new_article, publish_article, create_new_blog
from test_tool.settings import PRODUCTION

from tests import test_data


class BlogTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print('*Blog')
        if PRODUCTION:
            raise SkipTest("these tests shouldn't be runned on production")
        cls.session = test_data.session
        cls.browser_blogger = test_data.browser_blogger
        cls.browser = test_data.browser_guest

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """
        Create a new blog record and check it on front-end.
        It's prerequisite for other tests in this testcase.
        """
        self.blog_title = id_generator()
        self.blog_content = ' '.join([id_generator() for i in range(20)])  # 20 random "words"
        create_new_blog(self.browser_blogger, self.blog_title)
        self.edit_url = self.browser_blogger.current_url
        self.webcode = publish_article(self.browser_blogger, self.blog_content)

    def tearDown(self):
        pass

    def test_add_blog_record(self):
        """
        Create a new blog record and check it on front-end.
        """
        self.browser.get(navigate(self.webcode))
        result_title = self.browser.find_element_by_xpath('//*[@id="wrapper"]/div[4]/section/article[2]/h2').text
        self.assertEqual(self.blog_title, result_title,
                         "Blog record title not matches")
        result_content = self.browser.find_element_by_xpath('//*[@id="wrapper"]/div[4]/section/article[2]/p').text
        self.assertEqual(self.blog_content, result_content,
                         "Blog record content not matches")
