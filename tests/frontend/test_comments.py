from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import navigate, get_or_refresh
from test_tool.helpers.actions.frontend.article import open_first_article
from test_tool.helpers.actions.admin.comments import find_comment_element_on_backend, recommend_comment
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
        cls.posted_comment = add_comment(cls.browser_user)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def verify_is_comment_in_list(self, comments_list):
        self.assertTrue(
            max(
                comment['subject'] == unicode(self.posted_comment['subject'])
                and comment['content'] == unicode(self.posted_comment['content'])
                for comment in comments_list.values()
            ),
            'Posted comment is not in appropriate list.'
        )

    def test_normal_comment(self):
        """
        Post a normal comment
        """
        comments = get_all_comments_contents(self.browser_user)
        self.verify_is_comment_in_list(comments)

    def test_recommended_comment(self):
        """
        Post a comment and make it Recommended
        """
        get_or_refresh(self.browser_admin, '/admin/comment')
        comment_element = find_comment_element_on_backend(self.browser_admin, self.posted_comment['content'])
        recommend_comment(self.browser_admin, comment_element)
        self.browser_user.refresh()
        recommended_comments = get_all_comments_contents(self.browser_user, 'recommended')
        self.verify_is_comment_in_list(recommended_comments)
