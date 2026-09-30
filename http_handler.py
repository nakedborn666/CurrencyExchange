import traceback
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from path_parser import parser_obj
from serializer import serialize_data_to_json
from router import run_router
from exceptions.exception_handler import exception_handler


class MyHandler(BaseHTTPRequestHandler):


    def send_response_json(self, code, data):
        body = serialize_data_to_json(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


    def do_GET(self):
        controller = self.server.controller

        try:
            request = parser_obj.parse(self.command, self.path)
            valid_route = run_router(request.method, request.route, controller)
            result = valid_route(request)

        except Exception as e:
            code, message = exception_handler(e)
            self.send_response_json(code, message)

        else:
            self.send_response_json(200, result)


    def do_POST(self):
        controller = self.server.controller

        try:
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length).decode("utf-8")
            data = parse_qs(body, keep_blank_values=True)
            data_list = {k: v[0] for k, v in data.items()}
            request = parser_obj.parse(self.command, self.path, form=data_list)
            valid_route = run_router(request.method, request.route, controller)
            result = valid_route(request)

        except Exception as e:
            code, message = exception_handler(e)
            self.send_response_json(code, message)

        else:
            self.send_response_json(201, result)


    def do_PATCH(self):
        controller = self.server.controller

        try:
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length).decode("utf-8")
            data = parse_qs(body, keep_blank_values=True)
            data_list = {k: v[0] for k, v in data.items()}
            request = parser_obj.parse(self.command, self.path, form=data_list)
            valid_route = run_router(request.method, request.route, controller)
            result = valid_route(request)

        except Exception as e:
            traceback.print_exc()
            code, message = exception_handler(e)
            self.send_response_json(code, message)

        else:
            self.send_response_json(200, result)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()





#python -m http.server 8080 --bind 127.0.0.1