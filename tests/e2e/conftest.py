import os

from playwright.sync_api import Playwright
import pytest

from tests.e2e.utils.playwright_config import playwright_config_base, playwright_tear_down_base

HEADLESS = False
PAGE_URL = os.getenv('PAGE_URL')


@pytest.fixture(scope='session')
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


@pytest.fixture
def your_page_or_driver_name(browser, playwright: Playwright, request, web_session_driver):
    no_cookie = request.node.get_closest_marker('no_cookie')

    storage = None if no_cookie else web_session_driver
    page, context, browser = playwright_config_base(playwright, PAGE_URL, browser, storage, headless=HEADLESS)
    try:
        yield page
    finally:
        playwright_tear_down_base(context)
