from selenium.webdriver.common.by import By


class OrderFeedLocators:
    """Локаторы страницы «Лента заказов»."""

    # Заголовок страницы
    FEED_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")

    # Счётчики
    TOTAL_ORDERS_COUNTER = (By.XPATH,
            "//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'OrderFeed_number')]",)
    TODAY_ORDERS_COUNTER = (By.XPATH,
            "//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'OrderFeed_number')]",)

    # Раздел «В работе»
    IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]")
    IN_PROGRESS_ORDERS = (
        By.XPATH,
        "//ul[contains(@class, 'OrderFeed_orderListReady')]//li",
    )