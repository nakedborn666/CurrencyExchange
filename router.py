
from exceptions.exceptions import RouteNotExistsError



def run_router(method, route, controller):
    routes = {("GET", "currencies"): controller.get_currencies,
              ("POST", "currencies"): controller.post_currencies,
              ("GET", "currency"): controller.get_currency,
              ("GET", "exchangerates"): controller.get_all_rates,
              ("POST", "exchangerates"): controller.post_exchangerate,
              ("PATCH", "exchangerate"): controller.patch_exchangerate,
              ("GET", "exchangerate"): controller.get_rate,
              ("GET", "exchange"): controller.get_exchange
              }



    try:

        result = routes[method, route]
    except KeyError:
        raise RouteNotExistsError

    return result

