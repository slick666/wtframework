##########################################################################
# This file is part of WTFramework.
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################


from tests.flows.search_flows import perform_search
from tests.pages.search_page import ISearchPage
from tests.pages.www_google_com import GoogleSearchPage
from tests.pages.www_yahoo_com import YahooSearchPage
from tests.testdata.settings import get_search_provider
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.utils.test_utils import do_and_ignore
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
import unittest

# Extend the WTFBaseTest to get access to WTF added features like
# taking screenshot on test failure.


class Test(WTFBaseTest):

    def tearDown(self):
        "This tear down will close the current allocated webdriver"

        # do_and_ignore() is a handle wrapper that let's you run a statement
        # and not care if it errors or not.  This is helpful for tearDown
        # routines where the success/failure is not part of the test result.
        do_and_ignore(lambda: WTF_WEBDRIVER_MANAGER.close_driver())

    def test_basic_example(self):
        "Displays a simple PageObject instantiation example."

        # WTF_WEBDRIVER_MANAGER provides a easy to access to
        # the webdriver.  A web browser will be instantiated
        # according to your config settings.
        # - see 'selenium' settings in 'configs/default.yaml'
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()

        # Simple navigation
        webdriver.get("http://www.google.com")

        # Use the PageFactory class to instantiate your page.
        google_page = PageFactory.create_page(GoogleSearchPage, webdriver)

        # With your PageObject instantiated, you can call it's methods.
        google_page.search("hello world")

        self.assertTrue(google_page.result_contains("hello world"))

    def test_example_using_abstract_interfaces(self):
        "Demonstrates creating PageObjects using Abstract Factory pattern."
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get("http://www.google.com")

        # Notice I don't need specify GoogleSearchPage specifically, and
        # able to construct a ISearchPage of the correct type.
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        self.assertEqual(GoogleSearchPage, type(search_page))

        webdriver.get("http://www.yahoo.com")
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        self.assertEqual(YahooSearchPage, type(search_page))

    def test_using_flows(self):
        """
        Demonstrate abstracting out several steps into 1 call into a flow

        Let's say we have 2 or 3 steps that are repeated over and over again.
        Then it's a good idea to make it a workflow ('flow'), that can be 
        reused between different tests.
        """
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        search_page = perform_search("hello world", webdriver)
        self.assertTrue(search_page.result_contains("hello world"))

    def test_using_the_testdata(self):
        """
        Demonstrates getting a setting via testdata package, and WTF_CONFIG_READER

        By default it'll use google.com, but you can add this line in the config file 
        (by default it's default.yaml) You can override this setting.

        Insert the line below and run again to see this same test run in Yahoo.

            search_provider: http://www.yahoo.com

        By creating  testdata functions to abstract directly accessing WTF_CONFIG_READER, 
        we can reduce the number of hard coded strings that needs to be refactored if 
        configuration settings need to be refactored.
        """
        search_url = get_search_provider()
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(search_url)
        search_page = PageFactory.create_page(ISearchPage, webdriver)
        search_page.search("hello world")
        self.assertTrue(search_page.result_contains("hello world"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
