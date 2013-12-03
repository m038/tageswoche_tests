from unittest import TestCase, SkipTest
from selenium.webdriver.support.ui import Select
from datetime import timedelta

from test_tool.helpers.selenium_stuff import (
    get_or_refresh, get_current_time,
    wait_for_visible_by_css, wait_for_visible)
from test_tool.api.api_call import api_get
from test_tool.settings import PRODUCTION, LONG_AJAX, MAX_FOR_AJAX

from tests import test_data
from tests.additional_verifications import AdditionalVerifiesTestClass


class EventsTestCase(TestCase, AdditionalVerifiesTestClass):

    @classmethod
    def setUpClass(cls):
        print('*Events')
        if not PRODUCTION:
            raise SkipTest("these tests can be runned only on production")
        cls.session = test_data.session
        cls.current_date = get_current_time().strftime('%Y-%m-%d')
        cls.browser = test_data.browser_guest

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def wait_for_loading_bar_to_dissapear(self):
        wait_for_visible_by_css(self.browser, LONG_AJAX,
                                'figure.loading_block_events', until_not=True)

    def open_agenda(self):
        get_or_refresh(self.browser, '/agenda')
        self.wait_for_loading_bar_to_dissapear()

    def test_agenda_date(self):
        """
        Check if agenda date is actual
        """
        self.open_agenda()
        self.assertIn(self.current_date, self.browser.current_url)

    def test_list_of_regions(self):
        """
        List of regions, value in dropdown select is same as region_name in API
        """
        api_result = api_get(
            '/api/events',
            self.session,  params={
                'date': self.current_date,
                'region': 'kanton-basel-stadt',
                'genre': 'theater',
                'version': 1,
                'client': 'ipad',
            }
        )
        api_name_list = [item['region_name']
                         for item in api_result['regions'][:-1]]
        api_id_list = [item['region_id']
                       for item in api_result['regions'][:-1]]

        self.open_agenda()
        cities_select = Select(self.browser.find_element_by_id('wo'))
        frontend_name_list = [element.text
                              for element in cities_select.options]
        frontend_id_list = [element.get_attribute('value')
                            for element in cities_select.options]

        self.assertEqual(api_name_list, frontend_name_list,
                         "Cities names differs in API and on frontend.")
        self.assertEqual(api_id_list, frontend_id_list,
                         "Cities IDs differs in API and on frontend.")

    def test_morgen(self):
        """
        When select Morgen in calendar URL contains current date +1 day
        """
        self.open_agenda()
        calendar_link = self.browser.find_element_by_id('datapicker-button')
        calendar_link.click()
        morgen_link = wait_for_visible(
            self.browser, MAX_FOR_AJAX,
            lambda br:
            br.find_element_by_xpath('//*[@id="top-calendar"]/ul/li[2]/a'))
        morgen_link.click()
        self.wait_for_loading_bar_to_dissapear()

        tomorrow_date = (get_current_time() + timedelta(days=1))\
            .strftime('%Y-%m-%d')
        self.assertIn(tomorrow_date, self.browser.current_url)
