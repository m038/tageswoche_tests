from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
from test_tool.api.sections.articles import list as api_list

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

    def verify_playlist(self, section_id, uri):

        check_results = 11

        articles_links_api = [
            {
                'link': result['link'],
                'article_id': result['article_id'],
                'url': result['url'],
            }
            for result in api_list(self.session, section_id)
        ]

        self.browser.get(navigate(uri))
        articles_links_frontend = [result.get_attribute('href') for result in
            self.browser.find_elements_by_css_selector('article h2 a')
        ]

        for i in range(check_results):
            if articles_links_api[i]['link']:
                self.assertEqual(articles_links_api[i]['url'], articles_links_frontend[i],
                    '{0}-st article in {1}-st playlist not matches'.format(i, section_id))
            else:
                self.assertIn(str(articles_links_api[i]['article_id']), articles_links_frontend[i],
                    '{0}-st article in {1}-st playlist not matches'.format(i, section_id))

    def test_playlist_frontpage(self):
        """
        check if frontpage (http://tageswoche.ch) contains URLs of 11 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=6, uri='/')
