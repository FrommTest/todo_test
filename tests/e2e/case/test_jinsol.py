from playwright.sync_api import expect


def test_check_deployment_url(jinsol_test):
    page = jinsol_test

    expected_url = 'https://gray-cliff-009510f00.4.azurestaticapps.net/'
    expect(page).to_have_url(expected_url)
