from clients.http import get_json
from clients.exceptions import NotFoundError, ExternalServiceError

def get_rate(currency: str) -> float:
    url = f"https://api.frankfurter.dev/v2/rate/{currency}/RUB"

    try:
        data = get_json(url)
    except ExternalServiceError:
        raise NotFoundError(f"Currency {currency} not found")

    if "rate" not in data:
        raise ValueError("Отсутствует поле rate")

    rate = data['rate']

    return rate