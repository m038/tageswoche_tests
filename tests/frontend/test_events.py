from unittest import TestCase, SkipTest

from test_tool.helpers.selenium_stuff import (navigate, get_or_refresh, get_current_time,
                                              wait_for_visible_by_css)
from test_tool.settings import PRODUCTION, LONG_AJAX

from tests import test_data
from tests.additional_verifications import AdditionalVerifiesTestClass

class EventsTestCase(TestCase, AdditionalVerifiesTestClass):

    @classmethod
    def setUpClass(cls):
        print('*Events')
        if not PRODUCTION:
            raise SkipTest("these tests can be runned only on production")
        cls.current_date = get_current_time().strftime('%Y-%m-%d')
        cls.browser = test_data.browser_guest

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_agenda_date(self):
        """
        Check if agenda date is actual
        """
        get_or_refresh(self.browser, '/agenda')
        wait_for_visible_by_css(self.browser, LONG_AJAX, '#event_agenda_results h2')
        self.assertIn(self.current_date, self.browser.current_url)
