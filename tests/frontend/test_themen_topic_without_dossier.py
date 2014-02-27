from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
from test_tool.api.api_call import api_get

from tests.additional_verifications import AdditionalVerifiesTestClass
from tests import test_data


class ThemenPageWithoutDossierTestCase(TestCase, AdditionalVerifiesTestClass):

    @classmethod
    def setUpClass(cls):
        print('*Topic/Themen Topic page without dossier')
        cls.session = test_data.session
        cls.browser = test_data.browser_guest
        cls.api_result = api_get(uri='/api/articles/list?topic_id=586', session=cls.session)
        cls.browser.get(navigate('/themen/Apple'))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_articles_number(self):
        """
        @TODO:        This test verifies if Solr* works on server and if topic page gives correct number of articles/articles/etc.
        """
        articles_count_frontend = len(self.browser.find_elements_by_css_selector('ul#results li'))
        articles_count_api = len(self.api_result)
        self.assertEqual(articles_count_api, articles_count_frontend,
                         "Articles number differs (API: {0}, Frontend: {1}).".format(
                             articles_count_api, articles_count_frontend
                         ))

    def test_add_topic_button(self):
        """
        This test verifies if topic page has a button needed to add topic into Meine Themen.
        """
        self.verify_text_in_selector('a[href="#theme-abonnieren-content"]', "Dieses Thema abonnieren")
