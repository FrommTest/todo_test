from playwright.sync_api import expect

from tests.e2e.conftest import PAGE_URL


def test_login(logged_in):
    page = logged_in.new_page()

    page.goto(PAGE_URL)

    expected_url = 'https://gray-cliff-009510f00.4.azurestaticapps.net/login'
    print(page.url)
    expect(page).to_have_url(expected_url)
