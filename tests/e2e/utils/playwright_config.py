import os
from typing import Optional

from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, ViewportSize

load_dotenv(verbose=True)
URL = os.getenv('URL')


def playwright_config_base(
    playwright: Playwright,
    target_url: str,
    browser: Browser | None = None,
    storage_state: str | None = None,
    headless: bool = False,
    permissions: Optional[list[str]] = None,
) -> tuple[Page, BrowserContext, Browser]:
    """
    Playwright 세션을 생성하고 target_url로 진입한 뒤 tuple[page, context, browser]을 반환합니다.
    :param browser: 브라우져
    :param permissions: Playwright 권한
    :param headless: 헤드리스 여부
    :param playwright: playwright instance
    :param target_url: str (해당 driver를 주입 시 이동할 url)
    :param storage_state: str | None (쿠키 / storage 값을 저장해서 사용할 시)
    :return: tuple[Page, BrowserContext, Browser]
    """
    if browser is None:
        browser = playwright.chromium.launch(headless=headless)
    vp: ViewportSize = {'width': 1600, 'height': 800}
    context = browser.new_context(
        viewport=vp,
        storage_state=storage_state,
        permissions=permissions,
        locale='ko-KR',
        timezone_id='Asia/Seoul',
    )

    page = context.new_page()
    page.goto(target_url, wait_until='domcontentloaded')
    page.wait_for_url(target_url)
    page.wait_for_load_state('domcontentloaded')

    return page, context, browser


def playwright_tear_down_base(context: BrowserContext):
    """
    context를 정리합니다.
    :param context: BrowserContext
    """
    context.close()
