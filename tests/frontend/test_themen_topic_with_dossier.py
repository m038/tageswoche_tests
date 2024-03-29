from unittest import TestCase

from test_tool.helpers.selenium_stuff import navigate
from test_tool.api.api_call import api_get

from tests.additional_verifications import AdditionalVerifiesTestClass
from tests import test_data


class ThemenPageWithDossierTestCase(TestCase, AdditionalVerifiesTestClass):

    @classmethod
    def setUpClass(cls):
        print('*Topic/Themen Topic page without dossier')
        cls.session = test_data.session
        cls.browser = test_data.browser_guest
        cls.api_result = api_get(
            uri='/api/dossiers/articles?dossier_id=745&client=ipad&version=1',
            session=cls.session)
        cls.browser.get(navigate('/themen/Messe%20Basel'))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_article_list(self):
        """
        Ubersicht
        """
        check_articles = 7

        article_links_frontend = [element.get_attribute('href') for element in
                                  self.browser.find_elements_by_css_selector(
                                      'section.dossier-section h2 a'
                                  )]
        self.assertEqual(len(article_links_frontend), check_articles)
        article_ids_api = [record['article_id'] for record in self.api_result]
        self.assertGreaterEqual(len(article_ids_api), check_articles)
        for i in range(check_articles):
            self.assertIn(
                str(article_ids_api[i]), article_links_frontend[i],
                "{0}-st article id not matches ({1}, {2}).".format(
                    i+1, article_ids_api[i], article_links_frontend[i]
                ))
