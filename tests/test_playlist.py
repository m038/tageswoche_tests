from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate, unescape
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

    def verify_playlist(self, section_id, uri, check_results):

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
                self.assertEqual(unescape(articles_links_api[i]['url']), articles_links_frontend[i],
                    '{n}-st article in {section_id}-st playlist not matches ({url_a}, {url_f})'.format(
                        n=i+1, section_id=section_id,
                        url_a=articles_links_api[i]['url'], url_f=articles_links_frontend[i]))
            else:
                self.assertIn(str(articles_links_api[i]['article_id']), articles_links_frontend[i],
                    '{n}-st article in {section_id}-st playlist not matches ({article_id}, {url_f})'.format(
                        n=i+1, section_id=section_id,
                        article_id=articles_links_api[i]['article_id'], url_f=articles_links_frontend[i]))

    def test_playlist_frontpage(self):
        """
        check if frontpage (http://tageswoche.ch) and it's second page are contain URLs of 15 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=6, uri='/', check_results=15)

    def test_playlist_basel(self):
        """
        check if frontpage (http://www.tageswoche.ch/basel) contains URLs of 14 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=7, uri='/basel', check_results=14)

    def test_playlist_schweiz(self):
        """
        check if frontpage (http://www.tageswoche.ch/schweiz) and it's second page are contain URLs of 15 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=8, uri='/schweiz', check_results=15)  # @TODO:18

    def test_playlist_international(self):
        """
        check if frontpage (http://www.tageswoche.ch/international) and it's second page are contain URLs of 15 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=9, uri='/international', check_results=15)  # @TODO:18

    def test_playlist_sport(self):
        """
        check if frontpage (http://www.tageswoche.ch/sport) and it's second page are contain URLs of 15 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=10, uri='/sport', check_results=15)  # @TODO:18

    def test_playlist_kultur(self):
        """
        check if frontpage (http://www.tageswoche.ch/kultur) and it's second page are contain URLs of 15 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=11, uri='/kultur', check_results=15)  # @TODO:18

    def test_playlist_leben(self):
        """
        check if frontpage (http://www.tageswoche.ch/leben) and it's second page are contain URLs of 15 first objects (attribute Rank) regarding to their article id.
        """
        self.verify_playlist(section_id=25, uri='/leben', check_results=15)  # @TODO:18
