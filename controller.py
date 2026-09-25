

from exceptions.exceptions import NullCurrencyCodeError, NullExchangeRateCodesError, ExchangeRateNotFound
from dto.currency_create_dto import CurrencyCreateDTO
from dto.exchange_rate_create_dto import ExchangeRateCreateDTO
from dto.exchange_rate_patch_dto import ExchangeRatePatchDTO

class Controller:
    def __init__(self, currency_service, exchange_rate_service):
        self.currency_service = currency_service
        self.exchange_rate_service = exchange_rate_service

    def get_currencies(self, request):
        return self.currency_service.get_all_currencies()


    def get_currency(self, request):
        if request.parameter == []:
            raise NullCurrencyCodeError
        else:
            code = request.parameter[0].upper()
            return self.currency_service.get_currency(code)


    def get_all_rates(self, request):
        return self.exchange_rate_service.get_all_rates()


    def get_rate(self, request):
        if request.parameter == []:
            raise NullExchangeRateCodesError
        base_currency, target_currency = request.parameter[0].upper(), request.parameter[1].upper()
        result = self.exchange_rate_service.get_rate(base_currency, target_currency)
        if result is None:
            raise ExchangeRateNotFound
        else:
            return result


    def get_exchange(self, request):
        base_currency, target_currency, amount = request.query.from_, request.query.to, request.query.amount
        return self.exchange_rate_service.get_exchange(base_currency, target_currency, amount)


    def post_currencies(self, request):
        currency_dto = CurrencyCreateDTO(**request.form)
        return self.currency_service.post_currency(currency_dto)


    def post_exchangerate(self, request):
        exchangerate_dto = ExchangeRateCreateDTO(**request.form)
        return self.exchange_rate_service.post_exchangerate(exchangerate_dto)


    def patch_exchangerate(self, request):
        patch_rate_dto = ExchangeRatePatchDTO(**request.form)
        if request.parameter == []:
            raise NullExchangeRateCodesError
        return self.exchange_rate_service.patch_exchangerate(request.parameter[0].upper(), request.parameter[1].upper(), patch_rate_dto)