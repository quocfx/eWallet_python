from http.server import BaseHTTPRequestHandler
from source.utils import CommonUtils
from source.service import AccountService
from source.utils import JWTUtils
import re
import json


class AccountController(BaseHTTPRequestHandler):
    def do_GET(self):
        # Start with "/account/" and end with "/token"
        if re.search('^/account/.*/token$', self.path):
            accountId = CommonUtils.extractPathVariable(self.path, '/account/', '/token')
            myAccount = AccountService.getAccountByAccId(accountId)
            if len(myAccount) == 0:
                self.send_response(400)
                self.end_headers()
            else:
                accId = myAccount[0]["accountId"]
                jwtRes = JWTUtils.generateJWTFromAccount(accId)
                # responseStr = json.dumps(jwtRes)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(jwtRes.encode(encoding='utf_8'))

    def do_POST(self):
        if re.search('/account/topup/*', self.path):
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                jwtStr = self.headers.get('Authentication')
                tokenJson = JWTUtils.extractJWT(jwtStr)
                topupResult = AccountService.topupAccount(jwtStr, jsonObj["accountId"], jsonObj["balance"])
                if topupResult is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    responseStr = json.dumps(topupResult)
                    self.wfile.write(responseStr.encode(encoding='utf_8'))
                else:
                    self.send_response(400, "failure")
                    self.end_headers()
        elif re.search('/account/*', self.path):
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                if CommonUtils.checkAccountTypes(jsonObj["accountType"]):
                    newObj = {
                        "accountType": jsonObj["accountType"],
                        "accountName": jsonObj["accountName"]
                    }
                    newAccount = AccountService.addNewAccount(newObj)
                    responseStr = json.dumps(newAccount)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(responseStr.encode(encoding='utf_8'))
                else:
                    self.send_response(400, "Bad Request: account type is not valid")
                    self.end_headers()
            else:
                self.send_response(400, "Bad Request: invalid data")
                self.end_headers()
