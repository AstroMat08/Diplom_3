from selenium.webdriver.common.by import By


class BaseLocators:
    """Локаторы, общие для всех страниц (шапка сайта)."""

    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']/parent::a")
    LOGO = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]//a")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[@href='/account']")