import allure
import time

from locators.base_locators import BaseLocators
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from utils.urls import Urls


class MainPage(BasePage):
    """Page Object главной страницы (конструктор бургеров)."""

    @allure.step("Открыть главную страницу")
    def open_main(self):
        self.open(Urls.BASE_URL)

    @allure.step("Перейти в раздел «Конструктор»")
    def go_to_constructor(self):
        self.click(BaseLocators.CONSTRUCTOR_BUTTON)
        self.wait_visible(MainPageLocators.BURGER_CONSTRUCTOR_BASKET)


    @allure.step("Перейти в раздел «Лента заказов»")
    def go_to_order_feed(self):
        self.click(BaseLocators.ORDER_FEED_BUTTON)

    @allure.step("Кликнуть по ингредиенту «Флюоресцентная булка»")
    def click_fluor_bun(self):
        self.click(MainPageLocators.FLUORESCENT_BUN)

    @allure.step("Кликнуть по ингредиенту «Соус Spicy-X»")
    def click_spicy_sauce(self):
        self.click(MainPageLocators.SPICY_SAUCE)

    @allure.step("Получить название ингредиента в модальном окне")
    def get_modal_ingredient_name(self) -> str:
        return self.get_text(MainPageLocators.MODAL_INGREDIENT_NAME)

    @allure.step("Закрыть модальное окно крестиком")
    def close_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self) -> bool:
        return not self.is_element_present(MainPageLocators.MODAL_WINDOW, timeout=5)

    @allure.step("Получить счётчик ингредиента «Флюоресцентная булка»")
    def get_fluor_bun_counter(self) -> int:
        text = self.get_text(MainPageLocators.COUNTER_FLUORESCENT_BUN)
        return int(text) if text else 0

    @allure.step("Добавить ингредиент в конструктор")
    def add_ingredient_to_constructor(self, ingredient_locator):
        """Добавляет ингредиент через JS drag-and-drop."""
        source = self.find(ingredient_locator)
        target = self.wait_visible(MainPageLocators.BURGER_CONSTRUCTOR_BASKET)

        self.execute_script("""
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();

            source.dispatchEvent(new DragEvent('dragstart', { bubbles: true, dataTransfer }));
            target.dispatchEvent(new DragEvent('dragover', { bubbles: true, dataTransfer }));
            target.dispatchEvent(new DragEvent('drop', { bubbles: true, dataTransfer }));
            source.dispatchEvent(new DragEvent('dragend', { bubbles: true, dataTransfer }));
        """, source, target)

    @allure.step("Нажать «Оформить заказ»")
    def place_order(self):
        self.wait_place_order_enabled()  # ждём, что кнопка станет активной
        self.click(MainPageLocators.PLACE_ORDER_BUTTON, timeout=15)

    @allure.step("Получить номер оформленного заказа")
    def get_order_number(self, timeout: int = 15) -> str:
        """Возвращает номер заказа из модалки, дожидаясь реального значения
        (не заглушки 9999)."""
        self.wait_visible(MainPageLocators.ORDER_MODAL)

        def is_real_number(_):
            text = self.get_text(MainPageLocators.ORDER_NUMBER).strip()
            return text if text and text != "9999" else False

        return self.wait_until(
            is_real_number,
            timeout=timeout,
            message="Модалка не сменила заглушку 9999 на реальный номер",
        )

    @allure.step("Перейти на страницу логина")
    def go_to_login(self):
        self.click(BaseLocators.PERSONAL_ACCOUNT_BUTTON)

    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str):
        self.find(BaseLocators.LOGIN_EMAIL_INPUT).send_keys(email)

    @allure.step("Ввести пароль")
    def enter_password(self, password: str):
        self.find(BaseLocators.LOGIN_PASSWORD_INPUT).send_keys(password)

    @allure.step("Нажать «Войти»")
    def submit_login(self):
        self.click(BaseLocators.LOGIN_SUBMIT_BUTTON)

    @allure.step("Войти: email={email}")
    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.submit_login()

    @allure.step("Дождаться перехода на главную")
    def wait_url_is_main(self):
        self.wait_url_contains(Urls.BASE_URL)

    @allure.step("Проверить, что открыт Конструктор")
    def is_constructor_opened(self, timeout: int = 10) -> bool:
        return self.wait_visible(MainPageLocators.CONSTRUCTOR_TITLE, timeout=timeout) is not None

    @allure.step("Проверить, что открыто модальное окно ингредиента")
    def is_ingredient_modal_opened(self, timeout: int = 10) -> bool:
        return self.wait_visible(MainPageLocators.MODAL_WINDOW, timeout=timeout) is not None

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self, timeout: int = 10) -> bool:
        return self.wait_invisible(MainPageLocators.MODAL_WINDOW, timeout=timeout)

    @allure.step("Проверить, что открыта Лента заказов")
    def is_order_feed_opened(self, timeout: int = 10) -> bool:
        from locators.order_feed_locators import OrderFeedLocators
        return self.wait_visible(OrderFeedLocators.FEED_TITLE, timeout=timeout) is not None

    @allure.step("Дождаться, что счётчик ингредиента больше {value}")
    def wait_counter_greater_than(self, value: int, timeout: int = 10) -> bool:
        def counter_grew(_):
            return self.get_fluor_bun_counter() > value

        self.wait_until(counter_grew, timeout=timeout, message=f"Счётчик не увеличился. Было: {value}")
        return True

    @allure.step("Дождаться, что кнопка «Оформить заказ» активна")
    def wait_place_order_enabled(self, timeout: int = 10):
        self.wait_until(
            lambda _: self.is_enabled(MainPageLocators.PLACE_ORDER_BUTTON),
            timeout=timeout,
            message="Кнопка «Оформить заказ» осталась disabled — ингредиент не добавился",
        )