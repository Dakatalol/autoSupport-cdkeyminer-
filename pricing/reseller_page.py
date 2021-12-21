import logging
import requests
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from core.base_page import BasePage


class Reseller(BasePage):
    _search_field = "//input[@id='searchInputDesktop']"
    _search_first_result = "//span[@class='name__title'][1]"
    _game_names = []
    _games_and_prices = {}
    _top_currency_listbox = "//div[@class='top-bar']//app-currency/ng-select[@role='listbox']"
    _usd_currency = "//span[.='USD']"
    _not_found_games_list = []
    _reseller_games_and_prices = {}
    _price_list = "//div[@class='offers-table table-responsive']//table[@class='table']//td[@class='price']"

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout = 5

    @staticmethod
    def get_all_games_response():
        return requests.get("https://app.cdkeyminer.com/allGames").json()

    def format_game_names(self):
        for games in self.get_all_games_response():
            raw_name = games['fullName']
            name = raw_name.replace('CD Key', '')
            another_name = name.replace('Global', '')
            clean_name = another_name.replace('DLC', '')
            self._game_names.append(clean_name.strip())
            price = games['price']
            self._games_and_prices[clean_name.strip()] = [price * 0.401]

    def navigate_to_reseller_page(self):
        self.driver.get('')
        self.wait_for_page_loaded()

    def change_to_usd_currency(self):
        self.is_clickable(self._top_currency_listbox)
        self.click(self._top_currency_listbox)
        self.is_clickable(self._usd_currency)
        self.click(self._usd_currency)

    def search_game_and_navigate(self, game_name):
        time.sleep(2)
        self.wait_for_page_loaded()
        self.type(self._search_field, game_name)
        time.sleep(2)
        self.type(self._search_field, " ")
        time.sleep(0.5)
        self.type(self._search_field, " ")
        try:
            self.is_visible('//span[contains(text(),"{}")]'.format(game_name))
            self.myclick('//span[contains(text(),"{}")]'.format(game_name))
            self.wait_for_page_loaded()
        except WebDriverException:
            self.clear(self._search_field)
            self._not_found_games_list.append(game_name)
            print("not found game:" + game_name)

    def collect_reseller_prices(self):
        for games in self._game_names:
            try:
                self.search_game_and_navigate(games)
            except WebDriverException:
                continue
            prices = []
            self.wait_for_page_loaded()
            self.send_keys('html', Keys.PAGE_DOWN)
            time.sleep(1)
            try:
                for content in self.get_elements(self._price_list):
                    price = content.text
                    price = price.replace('$', '')
                    price = price.strip()
                    prices.append(float(price))
            except WebDriverException:
                print("Price not found for:" + games)
            try:
                lowest_price = min(prices)
            except:
                lowest_price = 0
            prices.clear()
            self._games_and_prices[games].append(lowest_price)

    def delete_all_not_found_games(self):
        """deleting all not found games from the list"""
        for games in list(self._not_found_games_list):
            for our_key, our_value in list(self._games_and_prices.items()):
                if games == our_key:
                    del self._games_and_prices[our_key]

    def print_negative_result(self):
        print("their_price+2>our_price: ")
        for our_key, our_value in list(self._games_and_prices.items()):
            our_price = our_value[0]
            their_price = our_value[1]
            if their_price + 2 > our_price:
                value = float(our_value[0]) - float(our_value[1])
                print("Game: " + our_key)
                print("Our value:" + str(our_value[0]) + " " + "Their value:" + str(our_value[1]))
                print(value)

    def print_positive_results(self):
        print("our_price-(their_price+2)>5: ")
        for our_key, our_value in list(self._games_and_prices.items()):
            our_price = our_value[0]
            their_price = our_value[1]
            if our_price - (their_price + 2) > 5:
                value = float(our_value[0]) - float(our_value[1])
                print("Game: " + our_key)
                print("Our value:" + str(our_value[0]) + " " + "Their value:" + str(our_value[1]))
                print(value)
