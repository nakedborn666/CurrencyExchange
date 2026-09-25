from exceptions.exceptions import *
class CurrencyService:
    def __init__(self, currency_dao):
        self.currency_dao = currency_dao

    def get_all_currencies(self):
        return self.currency_dao.get_all_currencies()


    def get_currency(self, code):
        currency = self.currency_dao.get_currency_by_code(code)
        if currency is None:
            raise CurrencyNotFoundError
        return currency

    def post_currency(self, currency_data):
        self.currency_dao.post_currency(currency_data)
        return self.get_currency(currency_data.code)



