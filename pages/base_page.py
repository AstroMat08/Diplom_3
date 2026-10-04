import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
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
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Дождаться, что URL содержит: {part}")
    def wait_url_contains(self, part: str, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(part)
        )

    @allure.step("Дождаться условия: {condition}")
    def wait_until(self, condition, timeout: int = 15, message: str = ""):
        """Обёртка над WebDriverWait для нестандартных ожиданий."""
        return WebDriverWait(self.driver, timeout).until(condition, message=message)

    @allure.step("Выполнить JS: {script}")
    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def is_enabled(self, locator) -> bool:
        return self.find(locator).is_enabled()