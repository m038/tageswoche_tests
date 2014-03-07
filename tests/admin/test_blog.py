from unittest import TestCase, SkipTest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.helpers.selenium_stuff import (
    navigate, id_generator, accept_js_alert, dismiss_js_alert,
    wait_for_visible_text_by_css)
from test_tool.helpers.actions.admin.article import (
    edit_article, publish_blog, create_new_blog)
from test_tool.settings import PRODUCTION, MAX_WAIT

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
        # 20 random "words":
        self.blog_content = ' '.join([id_generator() for i in range(20)])
        create_new_blog(self.browser_blogger, self.blog_title)
        self.edit_url = self.browser_blogger.current_url
        self.webcode = publish_blog(self.browser_blogger, self.blog_content)

    def tearDown(self):
        pass

    def verify_blog_content_on_frontend(self, new_content):
        self.browser.get(navigate(self.webcode))
        result_title = self.browser.find_element_by_xpath(
            '//*[@id="wrapper"]/div[4]/section/article[2]/h2').text
        self.assertEqual(self.blog_title, result_title,
                         "Blog record title not matches")
        result_content = self.browser.find_element_by_xpath(
            '//*[@id="wrapper"]/div[4]/section/article[2]/p').text
        self.assertEqual(new_content, result_content,
                         "Blog record content not matches")

    def verify_blog_list_presence(self):
        try:
            wait_for_visible_text_by_css(
                self.browser_blogger, MAX_WAIT,
                'h1', 'Blog management', partial=True)
        except TimeoutException:
            self.fail("Blog list wasn't opened")

    def test_add_blog_record(self):
        """
        Create a new blog record and check it on front-end.
        """
        self.verify_blog_content_on_frontend(self.blog_content)

    def test_edit_blog_save_all(self):
        """
        Changing blog as editor - Save All
        """
        new_article_content = ' '.join([id_generator() for i in range(20)])
        edit_article(self.browser_blogger, new_article_content, action='save')
        self.verify_blog_content_on_frontend(new_article_content)

    def _edit_blog_close_without_save(self):
        """
        Changing blog as editor - Close and leave
        """
        self.skipTest("js alert")
        new_article_content = ' '.join([id_generator() for i in range(20)])
        edit_article(self.browser_blogger, new_article_content, action='close')
        WebDriverWait(self.browser_blogger, MAX_WAIT).until(accept_js_alert)
        self.verify_blog_content_on_frontend(self.blog_content)
        self.verify_blog_list_presence()

    def _edit_blog_close_with_save(self):
        """
        Changing blog as editor - Close and stay
        """
        self.skipTest("js alert")
        new_article_content = ' '.join([id_generator() for i in range(20)])
        edit_article(self.browser_blogger, new_article_content, action='close')
        WebDriverWait(self.browser_blogger, MAX_WAIT).until(dismiss_js_alert)
        self.verify_blog_content_on_frontend(self.blog_content)

    def test_edit_blog_save_and_close(self):
        """
        Changing blog as editor - Save and close
        """
        new_article_content = ' '.join([id_generator() for i in range(20)])
        edit_article(self.browser_blogger, new_article_content,
                     action='save_and_close')
        self.verify_blog_content_on_frontend(new_article_content)
        self.verify_blog_list_presence()
