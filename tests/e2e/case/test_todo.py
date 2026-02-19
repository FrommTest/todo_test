from playwright.sync_api import expect

PAGE_URL = 'https://black-stone-05a57af00.2.azurestaticapps.net/'


class TestTodoPage:
    def test_page_url(self, todo_onyu_page):
        expect(todo_onyu_page).to_have_url(PAGE_URL)

    def test_page_title_visible(self, todo_onyu_page):
        expect(todo_onyu_page).to_have_title('TODO')

    def test_app_title_visible(self, todo_onyu_page):
        app_title = todo_onyu_page.locator('#app-title')
        expect(app_title).to_be_visible()
        expect(app_title).to_have_text('ONYU')
