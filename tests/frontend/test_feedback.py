from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import navigate, get_or_refresh
from test_tool.helpers.actions.admin.feedback import find_feedback_element_on_backend, get_list_of_feedback
from test_tool.helpers.actions.frontend.feedback import add_feedback
from test_tool.settings import PRODUCTION

from tests import test_data


class FeedbackTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        print('*Feedback')
        if PRODUCTION:
            raise SkipTest("these tests shouldn't be runned on production")
        cls.browser_admin = test_data.browser_admin
        cls.browser_user = test_data.browser_user
        cls.browser_user.get(navigate('/'))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def verify_is_feedback_in_list(self, feedback_list):
        self.assertTrue(
            max(
                comment['subject'] == unicode(self.feedback['subject'])
                and comment['content'] == unicode(self.feedback['content'])
                for comment in feedback_list
            ),
            'Posted feedback is not in appropriate list.'
        )

    def test_feedback(self):
        """
        Leave a feedback message and check it's presense in admin backend
        """
        self.feedback = add_feedback(self.browser_user)
        get_or_refresh(self.browser_admin, '/admin/feedback')
        feedback_list = get_list_of_feedback(self.browser_admin)
        self.verify_is_feedback_in_list(feedback_list)
