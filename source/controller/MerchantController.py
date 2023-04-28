from http.server import BaseHTTPRequestHandler
from source.utils import CommonUtils
from source.service import MerchantService
import re
import json


class MerchantController(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/merchant/signup/*', self.path):
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                newMerchant = MerchantService.addNewMerchant(jsonObj["merchantName"], jsonObj["merchantUrl"])
                jsonStr = json.dumps(newMerchant)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(jsonStr.encode(encoding='utf_8'))
            else:
                self.send_response(400, "Bad Request: invalid data")
                self.end_headers()
