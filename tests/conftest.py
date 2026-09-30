# tests/conftest.py
import allure
import pytest
import requests
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.main_page import MainPage
from locators.base_locators import BaseLocators
from utils.urls import Urls

API_BASE = "https://stellarburgers.education-services.ru"

def _generate_email() -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"ui_test_{suffix}@yandex.ru"

def _register_user_via_api() -> dict:
    """Создаёт уникального пользователя через API и возвращает его данные."""
    email = _generate_email()
    password = "password123"
    name = "UITestUser"

    response = requests.post(
        f"{API_BASE}/api/auth/register",
        json={"email": email, "password": password, "name": name},
    )
    body = response.json()
    return {
        "email": email,
        "password": password,
        "name": name,
        "access_token": body.get("accessToken"),
    }

def _delete_user_via_api(access_token: str):
    """Удаляет пользователя через API (в постусловии)."""
    requests.delete(
        f"{API_BASE}/api/auth/user",
        headers={"Authorization": access_token},
    )

# ===== Фикстуры браузера =====

def _chrome_driver():
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def _firefox_driver():
    options = FirefoxOptions()
    options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"
    return webdriver.Firefox(options=options)

@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    browser = request.param
    with allure.step(f"Инициализация драйвера: {browser}"):
        drv = _chrome_driver() if browser == "chrome" else _firefox_driver()
    yield drv
    with allure.step("Закрытие драйвера"):
        drv.quit()

# ===== Фикстура авторизованного пользователя =====

@pytest.fixture
def authorized_user(driver):
    """Создаёт уникального пользователя через API, логинит через UI."""

    with allure.step("Предусловие: создание уникального пользователя через API"):
        user = _register_user_via_api()

    with allure.step(f"Авторизация через UI: {user['email']}"):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.click(BaseLocators.PERSONAL_ACCOUNT_BUTTON)

        # Ждём появления формы логина — поле Email имеет name="name" (!)
        email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, "//label[text()='Email']/following-sibling::input"))
            )
        email_input.send_keys(user["email"])

        # Поле пароля — стандартное, name="Пароль"
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))
            )
        password_input.send_keys(user["password"])

        # Кнопка «Войти»
        driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        # Ждём редиректа на главную
        WebDriverWait(driver, 10).until(EC.url_to_be(f"{API_BASE}/"))

    yield user

    with allure.step("Постусловие: удаление пользователя через API"):
        _delete_user_via_api(user["access_token"])

def _get_last_order_number(access_token: str) -> str:
    """Получает номер последнего заказа пользователя через API.
    Возвращает номер без ведущих нулей (как в UI ленты)."""
    response = requests.get(
        f"{API_BASE}/api/orders",
        headers={"Authorization": access_token},
        timeout=15,
    )
    body = response.json()
    orders = body.get("orders", [])
    if not orders:
        raise AssertionError("У пользователя нет заказов — заказ не создался")

    # Первый в списке — самый свежий (сервер сортирует по updatedAt desc)
    last_order = orders[0]
    return str(last_order["number"]).lstrip("0")