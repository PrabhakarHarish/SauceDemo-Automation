import pytest
from pages import LoginPage, InventoryPage, CheckoutPage

#Parameterized test login

@pytest.mark.parametrize(
    "username, expected_success",
    [
        ("standard_user", True),
        ("locked_out_user", False),
        ("problem_user", True),
    ],
)
async def test_login_variations(page, username, expected_success):

    login_page = LoginPage(page)

    await login_page.goto()
    await login_page.login(username, "secret_sauce")

    await page.pause()

    if expected_success:

        assert "inventory.html" in page.url

    else:

        error = page.locator("[data-test='error']")

        assert await error.is_visible()

        assert (
            await error.inner_text()
            == "Epic sadface: Sorry, this user has been locked out."
        )



# PART B - PARAMETERIZED PRODUCT PRICE TEST
@pytest.mark.parametrize(
    "product_name, expected_price",
    [
        ("Sauce Labs Backpack", "$29.99"),
        ("Sauce Labs Bike Light", "$9.99"),
        ("Sauce Labs Bolt T-Shirt", "$15.99"),
    ],
)
async def test_product_prices(page, product_name, expected_price):

    login_page = LoginPage(page)

    await login_page.goto()
    await login_page.login("standard_user", "secret_sauce")

    product = page.locator(".inventory_item").filter(has_text=product_name)
    actual_price = await product.locator(".inventory_item_price").inner_text()
    assert actual_price == expected_price

# ADD TO CART

async def test_add_to_cart(page):

    login_page = LoginPage(page)

    await login_page.goto()
    await login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)

    await inventory_page.add_backpack_to_cart()

    cart_badge = page.locator(".shopping_cart_badge")

    assert await cart_badge.inner_text() == "1"



# FULL CHECKOUT
async def test_full_checkout(page):

    login_page = LoginPage(page)

    await login_page.goto()
    await login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)

    await inventory_page.add_backpack_to_cart()
    await inventory_page.go_to_cart()

    checkout_page = CheckoutPage(page)

    await checkout_page.start_checkout()

    await checkout_page.fill_info(
        "Harish","Kumar","560688",
    )

    await checkout_page.finish_order()

    result = await checkout_page.get_confirmation()

    assert result == "Thank you for your order!"

# LOGOUT

async def test_logout(page):

    login_page = LoginPage(page)

    await login_page.goto()
    await login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(page)

    await inventory_page.logout()

    assert await login_page.login_btn.is_visible()



# pytest -v Parameterized_test.py
