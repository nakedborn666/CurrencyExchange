class RouteNotExistsError(Exception):
    pass

class CurrencyNotFoundError(Exception):
    pass

class CurrenciesNotFoundError(Exception):
    pass

class ExchangeRateNotFound(Exception):
    pass

class RateForExchangeNotFound(Exception):
    pass

class NullCurrencyCodeError(Exception):
    pass

class NullExchangeRateCodesError(Exception):
    pass

class NullQueryParamsError(Exception):
    pass

class CurrencyAlreadyExistsError(Exception):
    pass

class NullFormFieldError(Exception):
    pass

class CurrencyNotExistsInDBError(Exception):
    pass

class ExchangeRateAlreadyExistsError(Exception):
    pass


class ExchangeRateNotExistsInDBError(Exception):
    pass