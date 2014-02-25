from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate, get_true_text
from test_tool.api.sections.search import search as api_search

from tests import test_data


class SearchTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = test_data.session
        cls.browser = test_data.browser_guest
        print('*Search')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search(self):
        """
        This test verifies if Solr* works on server and if searching gives \
correct response.
        """
        search_query = "Basel"
        check_results = 5  # check first five search results

        search_resuls_api = [result['teaser'] for result
                             in api_search(self.session, search_query)]
        self.assertGreaterEqual(
            len(search_resuls_api), check_results,
            "{num} search results in API call for '{que}' query (need {need})."
            .format(num=len(search_resuls_api),
                    que=search_query, need=check_results)
        )

        self.browser.get(navigate(
            '/search/?q={search_query}'.format(search_query=search_query)))
        search_resuls_frontend = [get_true_text(result) for result in
                                  self.browser.find_elements_by_css_selector(
                                      'ul#results li > p')
                                  ]
        self.assertGreaterEqual(
            len(search_resuls_frontend), check_results,
            "{num} search results in frontend for '{que}' query (need {need})."
            .format(num=len(search_resuls_frontend),
                    que=search_query, need=check_results)
        )

        for i in range(check_results):
            self.assertEqual(search_resuls_frontend[i], search_resuls_api[i],
                             '{0}-st search result not matches'.format(i + 1))
