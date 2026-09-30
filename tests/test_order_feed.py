import allure
from selenium.webdriver.support.ui import WebDriverWait

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

        # Создаём заказ: перетаскиваем ингредиент в корзину
        main_page.go_to_constructor()
        main_page.drag_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)
        main_page.place_order()
        main_page.wait_invisible(MainPageLocators.ORDER_MODAL)

        main_page.go_to_order_feed()
        WebDriverWait(driver, 15).until(
            lambda d: order_feed.get_total_orders() > total_before,
            message=f"Счётчик не увеличился. Было: {total_before}",
        )

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается после заказа")
    def test_today_orders_counter_increases(self, driver, authorized_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        main_page.open_main()
        main_page.go_to_order_feed()
        today_before = order_feed.get_today_orders()

        main_page.go_to_constructor()
        main_page.drag_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)
        main_page.place_order()
        main_page.wait_invisible(MainPageLocators.ORDER_MODAL)

        main_page.go_to_order_feed()
        WebDriverWait(driver, 15).until(
            lambda d: order_feed.get_today_orders() > today_before,
            message=f"Счётчик не увеличился. Было: {today_before}",
        )

    @allure.title("Номер заказа появляется в разделе «В работе»")
    def test_order_number_appears_in_progress(self, driver, authorized_user):
        main_page = MainPage(driver)
        order_feed = OrderFeedPage(driver)

        main_page.open_main()
        main_page.wait_visible(MainPageLocators.PLACE_ORDER_BUTTON)

        main_page.drag_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)
        main_page.place_order()

        # get_order_number САМ ждёт, пока 9999 сменится на реальный номер
        order_number = main_page.get_order_number().lstrip("0")

        main_page.close_modal()
        main_page.wait_invisible(MainPageLocators.ORDER_MODAL)

        main_page.go_to_order_feed()
        WebDriverWait(driver, 30).until(
            lambda d: order_number in [
                el.text.strip().lstrip("0")
                for el in d.find_elements(*OrderFeedLocators.IN_PROGRESS_ORDERS)
            ],
            message=f"Заказ {order_number} не появился в разделе «В работе»",
        )