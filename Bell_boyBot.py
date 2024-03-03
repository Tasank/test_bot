import json
import requests
from config import keys

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = keys[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        # API взаимодействие
        payload = {}
        headers = {
            "apikey": ""
        }

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={sym_key}&amount={amount}"
        r = requests.request("GET", url, headers=headers, data=payload)

        status_code = r.status_code
        result = r.content
        n_price = json.loads(result)
        new_price = n_price.get('result')
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message