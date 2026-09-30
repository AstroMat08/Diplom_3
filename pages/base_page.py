import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовый класс для всех Page Object. Содержит обёртки над действиями Selenium."""

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator, timeout: int = 10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        # JS-клик обходит перекрытие другими элементами
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator, timeout: int = 10) -> str:
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_visible(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Дождаться исчезновения элемента: {locator}")
    def wait_invisible(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def is_element_present(self, locator, timeout: int = 5) -> bool:
        """Проверка наличия элемента без падения."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False