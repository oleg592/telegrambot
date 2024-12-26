import requests

class APIException(Exception):
    pass

class CryptoConverter:
    currency_map = {
        "евро": "EUR",
        "доллар": "USD",
        "рубль": "RUB"
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f'https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}'
        response = requests.get(url)
        data = response.json()

        if 'Response' in data and data['Response'] == 'Error':
            raise APIException(data['Message'])

        if quote not in data:
            raise APIException(f"Невозможно получить курс для {quote}.")

        return data[quote] * amount

    @classmethod
    def convert_currency(cls, currency: str) -> str:
        currency = currency.lower()
        if currency in cls.currency_map:
            return cls.currency_map[currency]
        else:
            raise APIException(f'Неизвестная валюта: "{currency}". Доступны: {", ".join(cls.currency_map.keys())}')