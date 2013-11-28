from unittest import TestCase, SkipTest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.helpers.selenium_stuff import navigate, id_generator, accept_js_alert, dismiss_js_alert
from test_tool.helpers.actions.admin.article import create_new_article, publish_article, edit_article
from test_tool.helpers.actions.frontend.article import open_first_article
from test_tool.helpers.actions.frontend.comments import add_comment
from test_tool.settings import PRODUCTION, MAX_WAIT

from tests import test_data


class CommentsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print('*Comments')
        if PRODUCTION:
            raise SkipTest("these tests shouldn't be runned on production")
        cls.browser_admin = test_data.browser_admin
        cls.browser_user = test_data.browser_user
        cls.browser_user.get(navigate('/'))
        open_first_article(cls.browser_user)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_normal_comment(self):
        add_comment(self.browser_user)
