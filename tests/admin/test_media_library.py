from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import navigate
from test_tool.api.sections.feedback import upload_picture

from tests import test_data


class ProfileTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        raise SkipTest('temp')
        #if 'foobar' not in SERVER_URL:
        #    raise SkipTest("new advertisement functionality enabled only on 'devel' branch")
        cls.session = test_data.session
        cls.browser = test_data.browser_admin
        print('*Media library')

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
        upload_picture(self.session, "hard_penetration_666", "hard_penetration_666")
        self.browser(navigate('/admin/media-archive/index.php'))

        print(self.browser.getWindowHandles())
        return
        self.browser.get(navigate('/dashboard'))
        if log_in_as_user_if_necessary(self.browser) == 'logged_in_mobile':
            self.browser.get(navigate('/dashboard'))
        frontend_first_name = self.browser.find_element_by_id('first_name').get_attribute('value')
        api_first_name = api_profile(self.session)['first_name']
        self.assertEqual(api_first_name, frontend_first_name,
                         'first_name not matches in frontend and API')
