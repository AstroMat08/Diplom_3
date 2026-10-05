import allure

from locators.main_page_locators import MainPageLocators
from pages.main_page import MainPage


@allure.feature("Конструктор")
class TestConstructor:

    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.go_to_order_feed()
        main_page.go_to_constructor()

        assert main_page.is_constructor_opened(), \
            "Заголовок «Соберите бургер» не отображается"

    @allure.title("Переход по клику на «Лента заказов»")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.go_to_order_feed()

        assert main_page.is_order_feed_opened(), \
            "Заголовок «Лента заказов» не отображается"

    @allure.title("Клик по ингредиенту открывает модальное окно с деталями")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.click_fluor_bun()

        assert main_page.is_ingredient_modal_opened(), \
            "Модальное окно ингредиента не открылось"

    @allure.title("Модальное окно закрывается кликом по крестику")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        main_page.click_fluor_bun()
        main_page.wait_visible(MainPageLocators.MODAL_WINDOW)

        main_page.close_modal()

        assert main_page.is_modal_closed(), \
            "Модальное окно не закрылось после клика по крестику"

    @allure.title("Счётчик ингредиента увеличивается при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        main_page.open_main()
        counter_before = main_page.get_fluor_bun_counter()

        main_page.add_ingredient_to_constructor(MainPageLocators.FLUORESCENT_BUN)

        assert main_page.wait_counter_greater_than(counter_before), \
            f"Счётчик не увеличился. Было: {counter_before}"