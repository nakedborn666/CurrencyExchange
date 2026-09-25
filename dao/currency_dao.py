from dto.currency_dto import CurrencyDTO
from exceptions.exceptions import CurrencyAlreadyExistsError
import sqlite3

currency_keys = ["id", "code", "name", "sign"]

class CurrencyDAO:
    def __init__(self, connection):
        self.connection = connection


    def get_all_currencies(self):
        select_cur = self.connection.execute("SELECT * FROM Currencies")
        currencies = select_cur.fetchall()
        currencies_dict = [dict(zip(currency_keys, currency)) for currency in currencies]
        result = []
        for currency in currencies_dict:
            currency = CurrencyDTO(**currency)
            result.append(currency)
        return result


    def get_currency_by_code(self, code):
        select_currencies = self.connection.execute("SELECT * FROM Currencies WHERE code = ?", (code,))
        currency = select_currencies.fetchone()
        if currency is None:
            return None
        else:
            currency_dict = dict(zip(currency_keys, currency))
            result = CurrencyDTO(**currency_dict)
            return result


    def post_currency(self, currency_data):
        currency_data = currency_data.model_dump()
        try:
            sql_query_currencies = "INSERT INTO Currencies (code, fullname, sign) VALUES (:code, :name, :sign)"
            self.connection.execute(sql_query_currencies, currency_data)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            if e.sqlite_errorcode == sqlite3.SQLITE_CONSTRAINT_UNIQUE:
                raise CurrencyAlreadyExistsError
            raise

