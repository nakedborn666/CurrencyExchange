from dto.currency_dto import CurrencyDTO
from dto.exchange_rate_dto import ExchangeRateDTO
from exceptions.exceptions import ExchangeRateAlreadyExistsError
import sqlite3
currency_keys = ["id", "name", "code", "sign"]


class ExchangeRateDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_rate_dto(self, row):
        exchange_rate_id = row[0]
        base_cur = dict(zip(currency_keys, row[1:5]))
        base_cur_dto = CurrencyDTO(**base_cur)
        target_cur = dict(zip(currency_keys, row[5:9]))
        target_cur_dto = CurrencyDTO(**target_cur)
        rate = row[-1]
        exchange_rate_dto = ExchangeRateDTO(id=exchange_rate_id, baseCurrency=base_cur_dto,
                                                targetCurrency=target_cur_dto, rate=rate)
        return exchange_rate_dto


    def get_all_rates(self):
        select_exchange_rates = self.connection.execute("""SELECT ExchangeRates.id, base.id, base.fullname, base.code, base.sign, target.id, target.fullname, target.code, target.sign, ExchangeRates.rate FROM ExchangeRates
                JOIN Currencies as base
                ON base.id = ExchangeRates.BaseCurrencyId
                JOIN Currencies as target
                ON target.id = ExchangeRates.TargetCurrencyId""")
        exchange_rates = select_exchange_rates.fetchall()
        result = []
        for row in exchange_rates:
            rate = self.get_rate_dto(row)
            result.append(rate)
        return result


    def get_rate(self, base_cur_code, target_cur_code):
        select_exchange_rate = self.connection.execute("""SELECT ExchangeRates.id, base.id, base.fullname, base.code, base.sign, target.id, target.fullname, target.code, target.sign, ExchangeRates.rate FROM ExchangeRates
                JOIN Currencies as base
                ON base.id = ExchangeRates.BaseCurrencyId
                JOIN Currencies as target
                ON target.id = ExchangeRates.TargetCurrencyId
                WHERE base.code = ? AND target.code = ?""", (base_cur_code, target_cur_code))
        exchange_rate = select_exchange_rate.fetchone()
        if exchange_rate is None:
            return None
        else:
            return self.get_rate_dto(exchange_rate)


    def post_exchangerate(self, base_id, target_id, rate):
        exchangerate_data = [base_id, target_id, float(rate)]
        try:
            sql_query_exchangerate = "INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)"
            self.connection.execute(sql_query_exchangerate, exchangerate_data)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise ExchangeRateAlreadyExistsError
            raise


    def patch_exchangerate(self, base_id, target_id, rate):
        exchangerate_data = [rate, base_id, target_id]
        try:
            sql_query_exchangerate = "UPDATE ExchangeRates SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?"
            self.connection.execute(sql_query_exchangerate, exchangerate_data)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise ExchangeRateAlreadyExistsError
            raise