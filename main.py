import argparse
import sys

from clients.exceptions import NotFoundError, ExternalServiceError
from processing.service import build_city_summary


def main():
    parser = argparse.ArgumentParser(description="Сводка по городу: погода и курс валюты")
    parser.add_argument("--city", required=True)
    parser.add_argument("--currency", default="USD")
    args = parser.parse_args()

    try:
        summary = build_city_summary(args.city, args.currency)
    except NotFoundError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(3)
    except ExternalServiceError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(4)

    weather = summary["weather"]
    rates = summary["rates"]

    print(f"Город: {summary['city']}")
    print(f"Погода: {weather['temp_c']}°C, {weather['description']}")
    print(f"Тёплая одежда: {'да' if weather['warm_clothes'] else 'нет'}")
    print(f"{rates['currency']}→RUB: {rates['rate_to_rub']}")
    print(f"Дорогой курс: {'да' if rates['expensive'] else 'нет'}")

    sys.exit(0)


if __name__ == "__main__":
    main()