import pytest_asyncio
from playwright.async_api import async_playwright

@pytest_asyncio.fixture
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()

        await context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = await context.new_page()

        yield page
        await context.tracing.stop(path="trace.zip")

        await context.close()
        await browser.close()
