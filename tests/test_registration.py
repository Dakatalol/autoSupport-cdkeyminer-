import pytest
import time

from pages.registration_page import Registration


@pytest.mark.smoke
def test_verify_registration_account_field_is_present(driver):
    Registration(driver).logger.info("Verify Registration account field is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._username_field)


@pytest.mark.smoke
def test_verify_registration_password_field_is_present(driver):
    Registration(driver).logger.info("Verify Registration password field is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._password_field)


@pytest.mark.smoke
def test_verify_registration_repeat_password_field_is_present(driver):
    Registration(driver).logger.info("Verify Registration password field is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._repeat_password_field)


@pytest.mark.smoke
def test_verify_registration_email_field_is_present(driver):
    Registration(driver).logger.info("Verify email field is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._email_field)


@pytest.mark.smoke
def test_verify_registration_terms_and_conditions_link_is_present(driver):
    Registration(driver).logger.info("Verify terms and conditions link is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._terms_and_condition_link)


@pytest.mark.smoke
def test_verify_registration_privacy_policy_link_is_present(driver):
    Registration(driver).logger.info("Verify privacy policy link is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._privacy_policy_link)


@pytest.mark.smoke
def test_verify_registration_terms_and_conditions_checkbox_is_present(driver):
    Registration(driver).logger.info("Verify Registration terms and conditions is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._terms_and_condition_check_box)


@pytest.mark.smoke
def test_verify_registration_privacy_policy_checkbox_is_present(driver):
    Registration(driver).logger.info("Verify Registration privacy policy checkbox is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._privacy_policy_check_box)


def test_verify_registration_i_am_18_years_older_checkbox_is_present(driver):
    Registration(driver).logger.info("Verify Registration i am 18 years older checkbox is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._i_am_18_years_older_check_box)


def test_verify_registration_register_button_is_present(driver):
    Registration(driver).logger.info("Verify Registration register button is present")
    Registration(driver).navigate_to_register_page()
    assert Registration(driver).is_element_present(Registration._register_button)


@pytest.mark.smoke
def test_verify_empty_fields_validation(driver):
    Registration(driver).logger.info("Verify Registration field form validations for empty fields")
    Registration(driver).navigate_to_register_page()
    Registration(driver).wait_for_element_to_be_clickable(Registration._register_button)
    Registration(driver).click(Registration._register_button)
    Registration(driver).wait_for_page_loaded()
    Registration(driver).wait_for_element_to_be_clickable(Registration._validation_error_username)
    assert "Username must be 5 characters or more" in Registration(driver).get_text(
        Registration._validation_error_username)


@pytest.mark.smoke
def test_verify_empty_password_and_email_fields_validation(driver):
    Registration(driver).logger.info("Verify Registration field form validations for empty password and email field")
    Registration(driver).navigate_to_register_page()
    Registration(driver).wait_for_element_to_be_clickable(Registration._username_field)
    Registration(driver).type(Registration._username_field, "test123")
    Registration(driver).click(Registration._register_button)
    Registration(driver).wait_for_page_loaded()
    Registration(driver).wait_for_element_to_be_clickable(Registration._validation_error_password)
    assert "Password must be 5 characters or more" in Registration(driver).get_text(
        Registration._validation_error_password)


@pytest.mark.smoke
def test_verify_wrong_password_validation(driver):
    Registration(driver).logger.info("Verify Registration field form validations for wrong password field")
    Registration(driver).navigate_to_register_page()
    Registration(driver).type(Registration._username_field, "test123")
    Registration(driver).type(Registration._password_field, "Parola123")
    Registration(driver).type(Registration._repeat_password_field, "parola123")
    Registration(driver).type(Registration._email_field, "asd@abv.bg")
    Registration(driver).click(Registration._register_button)
    Registration(driver).wait_for_page_loaded()
    Registration(driver).wait_for_element_to_be_clickable(Registration._validation_password_doesnt_match)
    assert "Passwords don't match" in Registration(driver).get_text(Registration._validation_password_doesnt_match)


@pytest.mark.smoke
def test_verify_missed_checkboxes_validation(driver):
    Registration(driver).logger.info("Verify Registration field form validations for missed checkboxes")
    Registration(driver).navigate_to_register_page()
    Registration(driver).wait_for_element_to_be_clickable(Registration._username_field)
    Registration(driver).type(Registration._username_field, "test123")
    Registration(driver).type(Registration._password_field, "Parola123")
    Registration(driver).type(Registration._repeat_password_field, "Parola123")
    Registration(driver).type(Registration._email_field, "asd@abv.bg")
    Registration(driver).click(Registration._register_button)
    Registration(driver).wait_for_page_loaded()
    Registration(driver).wait_for_element_to_be_clickable(Registration._validation_must_agree_to_terms)
    assert "You must agree to the terms and conditions and privacy policy" in Registration(driver).get_text(
        Registration._validation_must_agree_to_terms)


@pytest.mark.smoke
def test_verify_missed_checkbox_for_age_validation(driver):
    Registration(driver).logger.info("Verify Registration field form validations for missed checkbox for age")
    Registration(driver).navigate_to_register_page()
    Registration(driver).type(Registration._username_field, "test123")
    Registration(driver).type(Registration._password_field, "Parola123")
    Registration(driver).type(Registration._repeat_password_field, "Parola123")
    Registration(driver).type(Registration._email_field, "asd@abv.bg")
    Registration(driver).click(Registration._register_button)
    Registration(driver).click(Registration._terms_and_condition_check_box)
    Registration(driver).click(Registration._privacy_policy_check_box)
    Registration(driver).wait_for_element_to_be_clickable(Registration._validation_for_age)
    assert "You must agree to the terms and conditions and privacy policy" in Registration(driver).get_text(
        Registration._validation_for_age)


# @pytest.mark.smoke
# def test_verify_user_is_able_to_register(driver):
#     Registration(driver).logger.info("Verify user is logged in successfully")
#     Registration(driver).navigate_to_register_page()
#     Registration(driver).Registration("test123", "Parola123", "Parola123", "pesho244@abv.bg")
#     Registration(driver).click(Registration._register_button)
#     Registration(driver).click(Registration._terms_and_condition_check_box)
#     Registration(driver).click(Registration._privacy_policy_check_box)
#     Registration(driver).click(Registration._i_am_18_years_older_check_box)
#     Registration(driver).wait_for_element_to_be_clickable(Registration._download_button)
#     assert Registration(driver).is_element_present(Registration._download_button)
