from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
from test_tool.api.sections.search import search as api_search

from tests import test_data


class SearchTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        #if 'foobar' not in SERVER_URL:
        #    raise SkipTest("new advertisement functionality enabled only on 'devel' branch")
        cls.session = test_data.session
        cls.browser = test_data.browser_embed

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_search(self):
        """
        This test verifies if Solr* works on server and if searching gives correct response.
        """
        search_query = "Basel"
        check_results = 5  # check first five search results

        search_resuls_api = [result['teaser'] for result in api_search(self.session, search_query)]

        self.browser.get(navigate('/search/?q={search_query}'.format(search_query=search_query)))
        search_resuls_frontend = [result.text for result in
            self.browser.find_elements_by_css_selector('ul#results li.article > p')
        ]

        for i in range(check_results):
            self.assertEqual(search_resuls_api[i], search_resuls_frontend[i],
                '{0}-st search result not matches'.format(i+1))
