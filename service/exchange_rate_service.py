from dto.exchange_rate_dto import ExchangeRateDTO
from dto.exchange_dto import ExchangeDTO
from exceptions.exceptions import *


class ExchangeRateService:
    def __init__(self, exchangerate_dao, currency_service):
        self.exchange_rate_dao = exchangerate_dao
        self.currency_service = currency_service

    def get_all_rates(self):
        return self.exchange_rate_dao.get_all_rates()

    def get_rate(self, base_cur_code, target_cur_code):
        return self.exchange_rate_dao.get_rate(base_cur_code, target_cur_code)



    def get_reverse_exchange(self, base_cur, target_cur):
        reverse_exchange = self.get_rate(target_cur, base_cur)
        if reverse_exchange:
            reverse_rate = round(1 / reverse_exchange.rate, 6)
            return ExchangeRateDTO(baseCurrency=reverse_exchange.targetCurrency, targetCurrency=reverse_exchange.baseCurrency, rate=reverse_rate)
        else:
            return None


    def get_cross_exchange(self, base_cur, target_cur):
        base_to_usd = self.get_rate(base_cur, "USD")
        usd_to_target = self.get_rate("USD", target_cur)
        if base_to_usd is None:
            base_to_usd = self.get_reverse_exchange(base_cur, "USD")
        if usd_to_target is None:
            usd_to_target = self.get_reverse_exchange("USD", target_cur)

        if base_to_usd is not None and usd_to_target is not None:
            cross_exchange_rate = round(base_to_usd.rate * usd_to_target.rate, 6)
            return ExchangeRateDTO(baseCurrency=base_to_usd.baseCurrency, targetCurrency=usd_to_target.targetCurrency, rate=cross_exchange_rate)

        return None


    def get_type_of_rate(self, base_cur, target_cur):
        direct = self.get_rate(base_cur, target_cur)
        if direct:
            return direct
        reverse = self.get_reverse_exchange(base_cur, target_cur)
        if reverse:
            return reverse
        cross = self.get_cross_exchange(base_cur, target_cur)
        if cross:
            return cross

        return None

    def get_exchange_dto(self, base_currency_dto, target_currency_dto, rate, amount, converted_amount):
        exchange_dto = ExchangeDTO(baseCurrency=base_currency_dto,
                                   targetCurrency=target_currency_dto, rate=rate,
                                   amount=amount, convertedAmount=converted_amount)
        return exchange_dto



    def get_exchange(self, base_cur, target_cur, amount):
        exchange_rate = self.get_type_of_rate(base_cur, target_cur)
        if exchange_rate is None:
            raise RateForExchangeNotFound
        else:
             converted_amount = amount * exchange_rate.rate
             result = self.get_exchange_dto(exchange_rate.baseCurrency, exchange_rate.targetCurrency, exchange_rate.rate, round(amount, 2), round(converted_amount, 2))
             return result





    def post_exchangerate(self, exchangerate_data):
        try:
            base_id = self.currency_service.get_currency(exchangerate_data.baseCurrencyCode).id
            target_id = self.currency_service.get_currency(exchangerate_data.targetCurrencyCode).id
            self.exchange_rate_dao.post_exchangerate(base_id, target_id, exchangerate_data.rate)
            return self.get_rate(exchangerate_data.baseCurrencyCode, exchangerate_data.targetCurrencyCode)
        except CurrencyNotFoundError:
            raise CurrencyNotExistsInDBError


    def patch_exchangerate(self, base_cur, target_cur, exchangerate_data):
        exchange_rate = self.get_rate(base_cur, target_cur)
        if exchange_rate is None:
            raise ExchangeRateNotExistsInDBError
        else:
            self.exchange_rate_dao.patch_exchangerate(exchange_rate.baseCurrency.id, exchange_rate.targetCurrency.id, float(exchangerate_data.rate))
            return self.get_rate(base_cur, target_cur)




