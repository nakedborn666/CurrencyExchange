from urllib.parse import urlparse, parse_qs
from exceptions.exceptions import NullQueryParamsError
from dto.query_dto import QueryDTO
from dto.request_dto import RequestDTO


class PathParser:

    def get_parsed_path(self, path):
        return urlparse(path)


    def get_split_path(self, path):
        if path.endswith("/"):
            return self.get_parsed_path(path).path.split("/")[1:-1]
        else:
            return self.get_parsed_path(path).path.split("/")[1:]


    def is_valid_path(self, path):
        split_path = self.get_split_path(path)
        if not split_path:
            return False

        route = split_path[0].lower()
        path_length = len(split_path)

        valid_endpoints_with_parameters = ("currency", "exchangerate")
        valid_endpoints_without_parameters = ("currencies", "exchangerates")
        valid_endpoint_with_query = ("exchange", )

        if route in valid_endpoints_with_parameters and path_length in (1, 2):
            return True
        elif (route in valid_endpoints_without_parameters or route in valid_endpoint_with_query) and path_length == 1:
            return True

        return False


    def request_to_dto(self, method, route, parameter, query):
        return RequestDTO(method=method, route=route, parameter=parameter, query=query)



    def parse(self, method, path, form=None):
        if not self.is_valid_path(path):
            return RequestDTO(method=method, route="", parameter=[], query=None, form=form)

        split_path = self.get_split_path(path)
        route = split_path[0].lower()
        parameter, query = [], None

        if route == "exchange":
            if not self.get_parsed_path(path).query:
                raise NullQueryParamsError
            parse_query = parse_qs(self.get_parsed_path(path).query)
            values = {k: v[0].upper() for k, v in parse_query.items()}
            query = QueryDTO(from_=values["from"], to=values["to"], amount=values["amount"])
        elif route == "exchangerate" and len(split_path) == 2:
            parameter = [split_path[1][:3].upper(), split_path[1][3:].upper()]
        elif len(split_path) == 2:
            parameter = [split_path[1].upper()]


        return RequestDTO(method=method, route=route, parameter=parameter, query=query, form=form)





parser_obj = PathParser()