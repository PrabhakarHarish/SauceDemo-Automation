from pages import LoginPage, InventoryPage, CheckoutPage


async def test_login(page):
    login = LoginPage(page)
    await login.goto()
    await login.login("standard_user", "secret_sauce")

    # assertion lives in the test
    assert await page.inner_text(".title") == "Products"


async def test_add_item_to_cart(page):
    login = LoginPage(page)
    await login.goto()
    await login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    await inventory.add_backpack_to_cart()

    # assert the cart badge shows 1 item
    assert await inventory.get_cart_count() == "1"


async def test_full_checkout(page):
    login = LoginPage(page)
    await login.goto()
    await login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    await inventory.add_backpack_to_cart()
    await inventory.go_to_cart()

    checkout = CheckoutPage(page)
    await checkout.start_checkout()
    await checkout.fill_info("Harish", "Kumar", "560001")
    await checkout.finish_order()

    assert await checkout.get_confirmation() == "Thank you for your order!"


async def test_logout(page):
    login = LoginPage(page)
    await login.goto()
    await login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    await inventory.logout()

    # logging out should land us back on the login button
    assert await page.locator("#login-button").is_visible()
