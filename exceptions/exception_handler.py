from pydantic import ValidationError

from exceptions.exceptions import *



exceptions_to_http = {CurrencyNotFoundError: (404, {"message": "Валюта не найдена"}),
                      CurrenciesNotFoundError: (404, {"message": "Валюты не найдены"}),
                      ExchangeRateNotFound: (404, {"message": "Обменного курса не найдено"}),
                      RateForExchangeNotFound: (404, {"message": "Не найдено ни одного обменного курса для данных валют"}),
                      KeyError: (400, {"message": "Неполный ввод данных"}),
                      ValidationError: (400, {"message": "Неверный ввод данных"}),
                      RouteNotExistsError: (404, {"message": "Данный маршрут отсутствует"}),
                      NullCurrencyCodeError: (400, {"message": "Код валюты отсутствует в адресе"}),
                      NullFormFieldError: (400, {"message": "Отсутствует нужное поле формы"}),
                      NullExchangeRateCodesError: (400, {"message": "Коды валют пары отсутствуют в адресе"}),
                      NullQueryParamsError: (400, {"message": "Отсутствуют параметры запроса"}),
                      CurrencyAlreadyExistsError: (409, {"message": "Валюта с таким кодом уже существует"}),
                      CurrencyNotExistsInDBError: (404, {"message": "Одна (или обе) валюта из валютной пары не существует в БД"}),
                      ExchangeRateAlreadyExistsError: (409, {"message": "Валютная пара с таким кодом уже существует"}),
                      ExchangeRateNotExistsInDBError: (404, {"message": "Валютная пара отсутствует в базе данных"})
                      }

def exception_handler(error):
    http_error = exceptions_to_http.get(type(error))
    if http_error is None:
        return (500, {"message": "Неизвестная ошибка"})
    return http_error