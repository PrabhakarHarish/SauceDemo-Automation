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


class InventoryPage:
    def __init__(self, page):
        self.page = page
        self.add_backpack_btn = page.locator("#add-to-cart-sauce-labs-backpack")
        self.cart_icon = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.menu_btn = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    async def add_backpack_to_cart(self):
        await self.add_backpack_btn.click()

    async def go_to_cart(self):
        await self.cart_icon.click()

    async def get_cart_count(self):
        return await self.cart_badge.inner_text()

    async def logout(self):
        await self.menu_btn.click()
        await self.logout_link.click()


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
        await self.confirmation_text.wait_for(state="visible")
        return await self.confirmation_text.inner_text()