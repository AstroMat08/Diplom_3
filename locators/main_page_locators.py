from selenium.webdriver.common.by import By


class MainPageLocators:
    """Локаторы главной страницы / конструктора."""

    # Заголовок «Соберите бургер»
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

    # Табы ингредиентов
    BUN_TAB = (By.XPATH, "//span[text()='Булки']")
    SAUCE_TAB = (By.XPATH, "//span[text()='Соусы']")
    FILLING_TAB = (By.XPATH, "//span[text()='Начинки']")

    # Ингредиенты
    FLUORESCENT_BUN = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']")
    SPICY_SAUCE = (By.XPATH, "//img[@alt='Соус Spicy-X']")

    # Модальное окно с деталями ингредиента
    MODAL_WINDOW = (By.XPATH, "//div[contains(@class, 'Modal_modal__content')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    MODAL_INGREDIENT_NAME = (
        By.XPATH,
        "//div[contains(@class, 'Modal_modal__content')]"
        "//*[text()='Флюоресцентная булка R2-D3']",
    )

    # Счётчик ингредиента «Флюоресцентная булка»
    COUNTER_FLUORESCENT_BUN = (
        By.XPATH,
        "//img[@alt='Флюоресцентная булка R2-D3']"
        "/ancestor::a//p[contains(@class, 'counter_counter__num')]",
    )

    # Кнопка «Оформить заказ»
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")

    # Модальное окно успешного заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")

    # Корзина конструктора — target для drag-and-drop
    BURGER_CONSTRUCTOR_BASKET = (
        By.XPATH,
        "//ul[contains(@class, 'BurgerConstructor_basket__list')]",
    )