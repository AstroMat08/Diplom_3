class Urls:
    """URL-адреса тестируемого приложения Stellar Burgers."""

    BASE_URL = "https://stellarburgers.education-services.ru"
    LOGIN = f"{BASE_URL}/login"
    REGISTER = f"{BASE_URL}/register"
    FORGOT_PASSWORD = f"{BASE_URL}/forgot-password"
    RESET_PASSWORD = f"{BASE_URL}/reset-password"
    ORDER_FEED = f"{BASE_URL}/feed"
    PROFILE = f"{BASE_URL}/account/profile"
    ORDER_HISTORY = f"{BASE_URL}/account/order-history"


class ApiUrls:
    """URL-адреса API (используются для подготовки данных в UI-тестах)."""

    BASE = "https://stellarburgers.education-services.ru/api"
    REGISTER = f"{BASE}/auth/register"
    LOGIN = f"{BASE}/auth/login"
    LOGOUT = f"{BASE}/auth/logout"
    USER = f"{BASE}/auth/user"
    ORDERS = f"{BASE}/orders"
    INGREDIENTS = f"{BASE}/ingredients"