from clients.rates import get_rate
from clients.weather import get_weather
from processing.preprocessing import is_cold, is_expensive


def build_city_summary(city: str, currency: str = "USD") -> dict:
    weather = get_weather(city)
    rate = get_rate(currency)
    
    weather["warm_clothes"] = is_cold(weather["temp_c"])
    
    return {
        "city": city,
        "weather": weather,
        "rates": {
            "currency": currency,
            "rate_to_rub": rate,
            "expensive": is_expensive(rate)
        }
    }