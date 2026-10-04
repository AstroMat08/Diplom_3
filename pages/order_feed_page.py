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
        elements = self.find_elements(OrderFeedLocators.IN_PROGRESS_ORDERS)
        return [el.text.strip() for el in elements if el.text]

    @allure.step("Дождаться появления заказа {order_number} в разделе «В работе»")
    def wait_order_in_progress(self, order_number: str, timeout: int = 60):
        def has_order(_):
            orders = [
                el.text.strip().lstrip("0")
                for el in self.find_elements(OrderFeedLocators.IN_PROGRESS_ORDERS)
            ]
            return order_number in orders

        self.wait_until(has_order, timeout=timeout, message=f"Заказ {order_number} не появился в разделе «В работе»")
        return True

    @allure.step("Проверить, что открыта Лента заказов")
    def is_opened(self, timeout: int = 10) -> bool:
        return self.wait_visible(OrderFeedLocators.FEED_TITLE, timeout=timeout) is not None

    @allure.step("Проверить, что счётчик «Выполнено за всё время» вырос")
    def wait_total_orders_greater_than(self, value: int, timeout: int = 60):
        def counter_grew(_):
            return self.get_total_orders() > value

        self.wait_until(counter_grew, timeout=timeout, message=f"Счётчик не увеличился. Было: {value}")
        return True
    
    @allure.step("Проверить, что счётчик «Выполнено за сегодня» вырос")
    def wait_today_orders_greater_than(self, value: int, timeout: int = 60):
        def counter_grew(_):
            return self.get_today_orders() > value

        self.wait_until(counter_grew, timeout=timeout, message=f"Счётчик не увеличился. Было: {value}")
        return True