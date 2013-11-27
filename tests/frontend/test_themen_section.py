from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate, unescape
from test_tool.api.sections.articles import list as api_list
from test_tool.api.api_call import api_get

from tests.additional_verifications import AdditionalVerifiesTestClass
from tests import test_data


class ThemenSectionTestCase(TestCase, AdditionalVerifiesTestClass):

    @classmethod
    def setUpClass(cls):
        print('*Topic/Themen Section page')
        cls.session = test_data.session
        cls.browser = test_data.browser_guest
        cls.api_result = api_get(uri='/api/dossiers/list?active=true&client=ipad', session=cls.session)
        cls.browser.get(navigate('/themen'))

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
            for result in api_list(self.session, section_id=section_id)
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

    def test_top(self):
        top_text_frontend = self.browser.find_element_by_css_selector('figure.mobile-pull-left big b').text
        top_text_api = unicode(self.api_result[0]['title'])
        self.assertEqual(top_text_api, top_text_frontend,
                         u"Top topic short text differs ('{0}','{1}').".format(top_text_api, top_text_frontend))

    def test_rest(self):
        articles_count_frontend = len(self.browser.find_elements_by_css_selector('div.mobile-list-view article'))\
            + len(self.browser.find_elements_by_css_selector('section > article'))
        articles_count_api = len(self.api_result)
        self.assertEqual(articles_count_api, articles_count_frontend,
                         "Articles number differs (API: {0}, Frontend: {1}).".format(
                             articles_count_api, articles_count_frontend
                         ))

    def test_list_of_topics(self):
        self.verify_selector('article.slideshow ul.dossier-litem-list li')
        self.verify_text_in_selector('ul.paging.content-paging li.caption', u"1/14")
