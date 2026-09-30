import allure
from selenium.webdriver.support.ui import WebDriverWait

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

    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_locator):
        """Эмулирует drag-and-drop ингредиента в корзину через JS-события.

        Ждёт, пока корзина конструктора станет видимой — это гарантирует,
        что React отрисовал её и навесил обработчики.
        """
        source = self.find(ingredient_locator)
        target = self.wait_visible(MainPageLocators.BURGER_CONSTRUCTOR_BASKET)

        self.driver.execute_script("""
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
        # Ждём, что кнопка кликабельна — значит, корзина не пуста
        self.click(MainPageLocators.PLACE_ORDER_BUTTON, timeout=15)

    @allure.step("Получить номер оформленного заказа")
    def get_order_number(self, timeout: int = 15) -> str:
        """Дожидается реального номера заказа в модалке.

        Фронтенд Stellar Burgers сначала показывает заглушку 9999,
        а через 1–3 секунды подставляет реальный номер. Метод
        ждёт, пока это произойдёт, и возвращает реальный номер.
        """
        self.wait_visible(MainPageLocators.ORDER_MODAL)

        def real_number(driver):
            text = self.get_text(MainPageLocators.ORDER_NUMBER).strip()
            return text if text and text != "9999" else False

        return WebDriverWait(self.driver, timeout).until(
            real_number,
            message="Модалка не сменила заглушку 9999 на реальный номер за 15 секунд",
        )