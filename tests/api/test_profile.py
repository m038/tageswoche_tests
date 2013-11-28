from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
from test_tool.api.sections.profile import profile as api_profile
from test_tool.settings import USER_MAIL, USER_PASS

from tests import test_data


class ProfileTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = test_data.session
        cls.browser = test_data.browser_user
        print('*Profile')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_profile(self):
        """
        This test verifies if user can login and if user dashboard gives correct info.
        """
        self.browser.get(navigate('/dashboard'))
        frontend_first_name = self.browser.find_element_by_id('first_name').get_attribute('value')
        api_first_name = api_profile(self.session, email=USER_MAIL, password=USER_PASS)['first_name']
        self.assertEqual(api_first_name, frontend_first_name,
                         'first_name not matches in frontend and API')
