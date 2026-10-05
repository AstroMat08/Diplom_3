import allure
import pytest
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.base_locators import BaseLocators

from pages.main_page import MainPage
from utils.api_client import UserApiClient
from utils.urls import Urls, ApiUrls


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


# ===== Фикстуры данных =====

@pytest.fixture
def user_data():
    """Только данные пользователя, без регистрации."""
    return {
        "email": UserApiClient.generate_email(),
        "password": "password123",
        "name": "UITestUser",
    }


@pytest.fixture
def registered_user(user_data):
    """Создаёт пользователя через API и удаляет в постусловии."""
    with allure.step("Предусловие: создание уникального пользователя через API"):
        body = UserApiClient.register(**user_data)
        access_token = body.get("accessToken")

    yield {**user_data, "access_token": access_token}

    with allure.step("Постусловие: удаление пользователя через API"):
        UserApiClient.delete(access_token)


@pytest.fixture
def authorized_user(driver, registered_user):
    """Авторизует пользователя через API и подставляет токены в localStorage.

    Обходит UI-логин, который не работает из-за особенностей фронтенда.
    Токены в localStorage React подхватывает автоматически после refresh.
    """
    with allure.step("Авторизация через API"):
        response = requests.post(
            ApiUrls.LOGIN,
            json={
                "email": registered_user["email"],
                "password": registered_user["password"],
            },
            timeout=15,
        )
        body = response.json()

        if response.status_code != 200:
            raise RuntimeError(f"API-логин упал: status={response.status_code}, body={body}")

        access_token = body["accessToken"]
        refresh_token = body["refreshToken"]

    with allure.step("Подстановка токенов в localStorage"):
        driver.get(Urls.BASE_URL)

        driver.execute_script(
            "window.localStorage.setItem('accessToken', arguments[0]);",
            access_token,
        )
        driver.execute_script(
            "window.localStorage.setItem('refreshToken', arguments[0]);",
            refresh_token,
        )

        # Перезагружаем страницу — React читает токены из localStorage
        driver.refresh()

    with allure.step("Проверка, что пользователь авторизован"):
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(BaseLocators.LOGIN_SUBMIT_BUTTON),
            message=f"Логин не прошёл. URL: {driver.current_url}",
        )

    return {
        **registered_user, 
        "access_token": access_token, 
        "refresh_token": refresh_token,
        }