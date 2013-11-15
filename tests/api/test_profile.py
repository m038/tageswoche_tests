from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
from test_tool.helpers.actions.auth import log_in_as_user_if_necessary
from test_tool.api.sections.profile import profile as api_profile

from tests import test_data


class ProfileTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        #if 'foobar' not in SERVER_URL:
        #    raise SkipTest("new advertisement functionality enabled only on 'devel' branch")
        cls.session = test_data.session
        cls.browser = test_data.browser_embed
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
        if log_in_as_user_if_necessary(self.browser) == 'logged_in_mobile':
            self.browser.get(navigate('/dashboard'))
        frontend_first_name = self.browser.find_element_by_id('first_name').get_attribute('value')
        api_first_name = api_profile(self.session)['first_name']
        self.assertEqual(api_first_name, frontend_first_name,
                         'first_name not matches in frontend and API')
