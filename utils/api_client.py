import random
import string

import requests

from utils.urls import ApiUrls


class UserApiClient:
    """Клиент для работы с пользователями через API."""

    @staticmethod
    def generate_email() -> str:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"ui_test_{suffix}@yandex.ru"

    @staticmethod
    def register(email: str, password: str, name: str) -> dict:
        response = requests.post(
            ApiUrls.REGISTER,
            json={"email": email, "password": password, "name": name},
            timeout=15,
        )
        body = response.json()
        assert response.status_code == 200, f"Не удалось создать пользователя: {body}"
        return body

    @staticmethod
    def delete(access_token: str) -> None:
        if access_token:
            requests.delete(
                ApiUrls.USER,
                headers={"Authorization": access_token},
                timeout=15,
            )

    @staticmethod
    def get_last_order_number(access_token: str) -> str:
        response = requests.get(
            ApiUrls.ORDERS,
            headers={"Authorization": access_token},
            timeout=15,
        )
        orders = response.json().get("orders", [])
        if not orders:
            raise AssertionError("У пользователя нет заказов")
        return str(orders[0]["number"]).lstrip("0")