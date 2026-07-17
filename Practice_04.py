import asyncio
from playwright.async_api import async_playwright


# ---------- PAGE 1: Login ----------
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_btn = page.locator("#login-button")

    async def goto(self):
        await self.page.goto("https://www.saucedemo.com/")

    async def login(self, user, pwd):
        await self.username.fill(user)
        await self.password.fill(pwd)
        await self.login_btn.click()


# ---------- PAGE 2: Product list (add item to cart) ----------
class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.add_backpack_btn = page.locator("#add-to-cart-sauce-labs-backpack")
        self.cart_icon = page.locator(".shopping_cart_link")

    async def add_backpack_to_cart(self):
        await self.add_backpack_btn.click()

    async def go_to_cart(self):
        await self.cart_icon.click()


# ---------- PAGE 3: Checkout ----------
class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.checkout_btn = page.locator("#checkout")
        self.first_name = page.locator("#first-name")
        self.last_name = page.locator("#last-name")
        self.zip_code = page.locator("#postal-code")
        self.continue_btn = page.locator("#continue")
        self.finish_btn = page.locator("#finish")
        self.confirmation_text = page.locator(".complete-header")

    async def start_checkout(self):
        await self.checkout_btn.click()

    async def fill_info(self, first, last, zip_code):
        await self.first_name.fill(first)
        await self.last_name.fill(last)
        await self.zip_code.fill(zip_code)
        await self.continue_btn.click()

    async def finish_order(self):
        await self.finish_btn.click()

    async def get_confirmation(self):
        return await self.confirmation_text.inner_text()


# ---------- THE ACTUAL TEST ----------
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        page = await browser.new_page()

        # Step 1: Login
        login_page = LoginPage(page)
        await login_page.goto()
        await login_page.login("standard_user", "secret_sauce")

        # Step 2: Add item to cart
        inventory_page = InventoryPage(page)
        await inventory_page.add_backpack_to_cart()
        await inventory_page.go_to_cart()

        # Step 3: Checkout
        checkout_page = CheckoutPage(page)
        await checkout_page.start_checkout()
        await checkout_page.fill_info("Harish", "Kumar", "560001")
        await checkout_page.finish_order()

        result = await checkout_page.get_confirmation()
        print("Result:", result)
        assert result == "Thank you for your order!"

        await browser.close()


asyncio.run(main())
