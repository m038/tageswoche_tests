#-*- coding: UTF-8 -*-
from unittest import TestCase
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from test_tool.helpers.selenium_stuff import navigate
from test_tool.settings import MAX_WAIT

from tests.additional_verifications import AdditionalVerifiesTestClass
from tests import test_data


class WidgetsTestCase(TestCase, AdditionalVerifiesTestClass):

    @classmethod
    def setUpClass(cls):
        print('*Widgets')
        cls.session = test_data.session
        cls.browser = test_data.browser_guest
        cls.browser.get(navigate('/'))

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def verify_image_link(self, img_link):
        """
        because even invalid image links returns 200 status code...
        """
        if not 'image/' in self.session.head(img_link, verify=False).headers['content-type']:
            self.fail("'{img_link}' don'y provides a valid image.".format(img_link=img_link))

    def test_weather(self):
        """
        Weather widget is presented on home page
        """
        self.verify_text_in_selector('a#weather-link span', '°C Basel')

    def test_omnitracker(self):
        """
        Omnitracker widget is presented on home page
        """
        self.verify_number_of_elements('article#ticker-sidebar-desktop section', 6)

    def test_good_comments(self):
        """
        Good comments widget is presented on home page
        """
        self.verify_selector('div.slideshow div.slide-item')

    def test_newsdesk(self):
        """
        Newsdesk widget is presented on home page
        """
        img_link = self.verify_selector('article.newsdeskMessage figure img').get_attribute('src')
        self.verify_image_link(img_link)
        self.verify_text_in_selectors_attribute('article.newsdeskMessage a', 'href', 'mailto:')

    def test_community(self):
        """
        Community widget is presented on home page
        """
        try:
            WebDriverWait(self.browser, MAX_WAIT).until(
                lambda br: True if
                len(br.find_elements_by_css_selector('article.community.omni-corner-box li.omni'))
                + len(br.find_elements_by_css_selector('article.community.omni-corner-box li.comment'))
                == 6 else None
            )
        except TimeoutException:
            self.fail("No enough of 'article.community.omni-corner-box li'")

    def test_link(self):
        """
        Link widget is presented on home page
        """
        self.verify_number_of_elements('section.recommend', 7)

    def test_debate(self):
        """
        Debate widget is presented on home page
        """
        self.verify_selector('div.debate-box.omni-corner-box li.ja')

    def test_ausgabe(self):
        """
        Ausgabe widget is presented on home page
        """
        img_link = self.verify_selector('div.frontpage-holder img').get_attribute('src')
        self.verify_image_link(img_link)

    def test_themen(self):
        """
        Themen widget is presented on home page
        """
        self.verify_number_of_elements('div.mobile-list-view.dossier-mobile-list div.two-columns article', 4)
