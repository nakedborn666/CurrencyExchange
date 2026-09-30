from http.server import HTTPServer
from controller import Controller
from dao.currency_dao import CurrencyDAO
from dao.exchange_rate_dao import ExchangeRateDAO
from http_handler import MyHandler
from service.currency_service import CurrencyService
from service.exchange_rate_service import ExchangeRateService


def create_server(db, host="0.0.0.0", port=8000):
    db.create_tables()
    db.seed_data()

    cur_dao_obj = CurrencyDAO(connection=db.connection)
    exchangerate_dao_obj = ExchangeRateDAO(db.connection)

    currency_service = CurrencyService(cur_dao_obj)
    exchangerate_service = ExchangeRateService(exchangerate_dao_obj, currency_service)

    server = HTTPServer((host, port), MyHandler)
    server.controller = Controller(currency_service, exchangerate_service)

    return server