from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import navigate
from test_tool.helpers.actions.frontend.article import open_first_article
from test_tool.helpers.actions.frontend.comments import add_comment, get_all_comments_contents
from test_tool.settings import PRODUCTION

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
        """
        Post a normal comment
        """
        posted_comment = add_comment(self.browser_user)
        comments = get_all_comments_contents(self.browser_user)
        self.assertTrue(
            max(
                comment['subject'] == unicode(posted_comment['subject'])
                and comment['content'] == unicode(posted_comment['content'])
                for comment in comments.values()
            ),
            'Posted comment is not in "all comments" list.'
        )
