import os
from typing import Optional

import allure
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, ViewportSize
import platform

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
        record_video_dir=VIDEO_PATH,
        locale='ko-KR',
        timezone_id='Asia/Seoul',
    )

    context.tracing.start(screenshots=True, snapshots=True)

    page = context.new_page()
    page.goto(target_url, wait_until='domcontentloaded')
    page.wait_for_url(target_url)
    page.wait_for_load_state('domcontentloaded')

    return page, context, browser

def pytest_sessionfinish():
    browser_name = os.getenv("BROWSER", "Chrome")
    os.makedirs('allure-results', exist_ok=True)
    with open('allure-results/environment.properties', 'w', encoding='utf-8') as f:
        f.write(f'OS={platform.platform()}\n')
        f.write(f"Browser={browser_name}\n")
        f.write(f'TODO_ONYU_ID={os.getenv("ONYU_ID")}\n')



TRACE_PATH = 'traces/'
VIDEO_PATH = 'videos/'


def playwright_tear_down_base(request, context: BrowserContext, page: Page):
    """
    리포트에 trace와 비디오를 첨부한 후 tracing,page,context,browser 자원을 정리합니다.
    .. seealso::
        `playwright_config_base: 해당 함수에서 반환된 자원을 parameter로 이용`
    :param request: node
    :param context: BrowserContext
    :param browser: Browser
    :param page: Page
    """
    try:
        trace_name = f'{request.node.name.split("[")[0]}_trace.zip'
        trace_path = f'{TRACE_PATH}/{trace_name}'
        context.tracing.stop(path=trace_path)

        with open(f'{trace_path}', 'rb') as trace_file:
            allure.attach(
                'npx playwright show-trace <ZIP 파일 이름>.zip',
                name='Trace 실행방법',
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(trace_file.read(), name=f'{trace_name}', attachment_type='application/zip')

        context.close()

        with open(page.video.path(), 'rb') as f:
            allure.attach(f.read(), name=f'web_{request.node.name}_video', attachment_type=allure.attachment_type.WEBM)

    except Exception as e:
        print.error(f'[teardown] failed: {e!r}')