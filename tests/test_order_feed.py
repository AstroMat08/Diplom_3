import allure

from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedLocators
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Счётчик «Выполнено за всё время» увеличивается после заказа")
    def test_total_orders_counter_increases(self, driver, authorized_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        main_page.open_main()
        main_page.go_to_order_feed()
        total_before = order_feed.get_total_orders()

        main_page.go_to_constructor()
        main_page.add_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)
        main_page.place_order()
        main_page.close_modal()
        main_page.wait_invisible(MainPageLocators.ORDER_MODAL)

        main_page.go_to_order_feed()

        assert order_feed.wait_total_orders_greater_than(total_before), \
            f"Счётчик «Выполнено за всё время» не увеличился. Было: {total_before}"

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается после заказа")
    def test_today_orders_counter_increases(self, driver, authorized_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        main_page.open_main()
        main_page.go_to_order_feed()
        today_before = order_feed.get_today_orders()

        main_page.go_to_constructor()
        main_page.add_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)
        main_page.place_order()
        main_page.close_modal()
        main_page.wait_invisible(MainPageLocators.ORDER_MODAL)

        main_page.go_to_order_feed()

        assert order_feed.wait_today_orders_greater_than(today_before), \
            f"Счётчик «Выполнено за сегодня» не увеличился. Было: {today_before}"

    @allure.title("Номер заказа появляется в разделе «В работе»")
    def test_order_number_appears_in_progress(self, driver, authorized_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        main_page.open_main()
        main_page.add_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)
        main_page.place_order()

        order_number = main_page.get_order_number().lstrip("0")

        main_page.close_modal()
        main_page.wait_invisible(MainPageLocators.ORDER_MODAL)
        main_page.go_to_order_feed()

        assert order_feed.wait_order_in_progress(order_number), \
            f"Заказ {order_number} не появился в разделе «В работе»"