from http.server import BaseHTTPRequestHandler
from source.controller.AccountController import AccountController
from source.controller.MerchantController import MerchantController
from source.controller.TransactionController import TransactionController


class RoutingRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/account"):
            AccountController.do_GET(self)

    def do_POST(self):
        if self.path.startswith("/merchant"):
            MerchantController.do_POST(self)
        elif self.path.startswith("/transaction"):
            TransactionController.do_POST(self)
        elif self.path.startswith("/account"):
            AccountController.do_POST(self)

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authentication")
        BaseHTTPRequestHandler.end_headers(self)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authentication")
        BaseHTTPRequestHandler.end_headers(self)
