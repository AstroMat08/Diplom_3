from selenium.webdriver.common.by import By


class BaseLocators:
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']/parent::a")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']/parent::a")
    LOGO = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]//a")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[@href='/account']")

    LOGIN_EMAIL_INPUT = (
        By.XPATH,
        "//label[text()='Email']/following-sibling::input",
    )
    LOGIN_PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[text()='Войти']")