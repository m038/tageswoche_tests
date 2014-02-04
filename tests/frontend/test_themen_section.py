from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
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

    def test_top(self):
        top_text_frontend = self.browser.find_element_by_css_selector('figure.mobile-pull-left big b').text
        top_text_api = self.api_result[0]['title']
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
