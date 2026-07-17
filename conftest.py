import pytest_asyncio
from playwright.async_api import async_playwright

@pytest_asyncio.fixture
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        page = await browser.new_page()
        yield page              # <-- the test runs at this point, using `page`
        await browser.close()