import allure

from locators.order_feed_locators import OrderFeedLocators
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    """Page Object страницы «Лента заказов»."""

    @allure.step("Получить счётчик «Выполнено за всё время»")
    def get_total_orders(self) -> int:
        text = self.get_text(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        return int(text)

    @allure.step("Получить счётчик «Выполнено за сегодня»")
    def get_today_orders(self) -> int:
        text = self.get_text(OrderFeedLocators.TODAY_ORDERS_COUNTER)
        return int(text)

    @allure.step("Получить список заказов «В работе»")
    def get_in_progress_orders(self) -> list:
        self.wait_visible(OrderFeedLocators.IN_PROGRESS_SECTION)
        elements = self.driver.find_elements(*OrderFeedLocators.IN_PROGRESS_ORDERS)
        return [el.text.strip() for el in elements if el.text]