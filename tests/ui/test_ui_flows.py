import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope='session')
def playwright_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope='function')
def page(playwright_instance):
    # Fresh isolated context for each test case
    context = playwright_instance.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


def perform_login(page, base_url):
    page.goto(f"{base_url}/login")
    page.fill("#username", "admin@retail.com")
    page.fill("#password", "Admin123!")
    page.click("#btn-submit-login")
    page.wait_for_url(f"{base_url}/orders")


def test_ui_01_valid_login(page, live_server_url):
    page.goto(f"{live_server_url}/login")
    page.fill("#username", "admin@retail.com")
    page.fill("#password", "Admin123!")
    page.click("#btn-submit-login")
    page.wait_for_url(f"{live_server_url}/orders")
    assert "/orders" in page.url
    expect(page.locator("#nav-orders")).to_be_visible()


def test_ui_02_invalid_login(page, live_server_url):
    page.goto(f"{live_server_url}/login")
    page.fill("#username", "admin@retail.com")
    page.fill("#password", "WrongPassword!")
    page.click("#btn-submit-login")
    expect(page.locator("#login-error-alert")).to_be_visible()
    expect(page.locator("#login-error-alert")).to_contain_text("Invalid email or password")


def test_ui_03_order_search(page, live_server_url):
    perform_login(page, live_server_url)
    page.fill("#search-input", "Alice")
    page.click("#btn-apply-filter")
    page.wait_for_selector("#orders-table")
    rows = page.locator(".order-row")
    assert rows.count() >= 1
    expect(rows.first).to_contain_text("Alice")


def test_ui_04_status_filter(page, live_server_url):
    perform_login(page, live_server_url)
    page.select_option("#status-select", "DELIVERED")
    page.click("#btn-apply-filter")
    page.wait_for_selector("#orders-table")
    rows = page.locator(".order-row")
    assert rows.count() >= 1
    for i in range(rows.count()):
        expect(rows.nth(i).locator(".status-badge")).to_contain_text("DELIVERED")


def test_ui_05_date_filter(page, live_server_url):
    perform_login(page, live_server_url)
    page.fill("#start-date", "2026-02-01")
    page.fill("#end-date", "2026-02-28")
    page.click("#btn-apply-filter")
    page.wait_for_selector("#orders-table")
    rows = page.locator(".order-row")
    assert rows.count() >= 1


def test_ui_06_view_order_details(page, live_server_url):
    perform_login(page, live_server_url)
    page.click("#btn-view-1")
    page.wait_for_selector("#order-title")
    expect(page.locator("#order-title")).to_contain_text("ORD-2026-0001")
    expect(page.locator("#customer-full-name")).to_contain_text("Alice Smith")
    expect(page.locator("#order-items-table")).to_be_visible()
    expect(page.locator("#order-total-amount")).to_contain_text("$268.65")


def test_ui_07_order_status_update(page, live_server_url):
    perform_login(page, live_server_url)
    page.goto(f"{live_server_url}/orders/5")  # PENDING order
    page.select_option("#new-status-select", "CONFIRMED")
    page.click("#btn-update-status")
    page.wait_for_selector("#current-status-badge")
    expect(page.locator("#current-status-badge")).to_contain_text("CONFIRMED")


def test_ui_08_empty_search_results(page, live_server_url):
    perform_login(page, live_server_url)
    page.fill("#search-input", "NONEXISTENT_CUSTOMER_XYZ")
    page.click("#btn-apply-filter")
    expect(page.locator("#no-orders-msg")).to_be_visible()
    expect(page.locator("#no-orders-msg")).to_contain_text("No orders found")


def test_ui_09_create_order_page_navigation(page, live_server_url):
    perform_login(page, live_server_url)
    page.click("#nav-create")
    page.wait_for_selector("#create-order-form")
    expect(page.locator("#customer_id")).to_be_visible()


def test_ui_10_analytics_page(page, live_server_url):
    perform_login(page, live_server_url)
    page.click("#nav-analytics")
    page.wait_for_selector("#kpi-total-orders")
    expect(page.locator("#kpi-total-orders")).not_to_have_text("--")
