import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.main_page_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedLocators
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.feature("Конструктор")
class TestConstructor:

    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.go_to_order_feed()

        main_page.go_to_constructor()

        title = main_page.get_text(MainPageLocators.CONSTRUCTOR_TITLE)
        assert "Соберите бургер" in title

    @allure.title("Переход по клику на «Лента заказов»")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()

        main_page.go_to_order_feed()

        WebDriverWait(driver, 10).until(EC.url_contains("/feed"))
        assert driver.current_url.endswith("/feed")

        order_feed = OrderFeedPage(driver)
        title = order_feed.get_text(OrderFeedLocators.FEED_TITLE)
        assert "Лента заказов" in title

    @allure.title("Клик по ингредиенту открывает модальное окно с деталями")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()

        main_page.click_fluor_bun()

        main_page.wait_visible(MainPageLocators.MODAL_WINDOW)
        modal_name = main_page.get_modal_ingredient_name()
        assert "Флюоресцентная булка" in modal_name

    @allure.title("Модальное окно закрывается кликом по крестику")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.click_fluor_bun()
        main_page.wait_visible(MainPageLocators.MODAL_WINDOW)

        main_page.close_modal()
        main_page.wait_invisible(MainPageLocators.MODAL_WINDOW)

    @allure.title("Счётчик ингредиента увеличивается при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()

        counter_before = main_page.get_fluor_bun_counter()

        main_page.drag_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)

        WebDriverWait(driver, 10).until(
            lambda d: main_page.get_fluor_bun_counter() > counter_before
        )
        counter_after = main_page.get_fluor_bun_counter()

        assert counter_after > counter_before