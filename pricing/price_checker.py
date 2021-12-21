import pytest

from pricing.reseller_page import Reseller


@pytest.mark.smoke
def test_prices(driver):
    Reseller(driver).format_game_names()
    Reseller(driver).navigate_to_reseller_page()
    Reseller(driver).change_to_usd_currency()
    Reseller(driver).collect_reseller_prices()
    Reseller(driver).delete_all_not_found_games()
    Reseller(driver).print_negative_result()
    Reseller(driver).print_positive_results()
