from http.server import BaseHTTPRequestHandler
from source.utils import CommonUtils
import re
import json
from source.service import TransactionService
from source.const.CommonEnum import TransactionType


class TransactionController(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/transaction/create/*', self.path):
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                jwtStr = self.headers.get('Authentication')
                newTrans = TransactionService.initTransaction(jwtStr, jsonObj)
                if newTrans is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    responseStr = json.dumps(newTrans)
                    self.wfile.write(responseStr.encode(encoding='utf_8'))
                else:
                    self.send_response(400, "failure")
                    self.end_headers()
        elif re.search('/transaction/confirm/*', self.path):
            resultResponse = {
                "code": "",
                "message": ""
            }
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                jwtStr = self.headers.get('Authentication')
                newTrans = TransactionService.confirmTransaction(jwtStr, jsonObj["transactionId"])
                if newTrans is not None:
                    if newTrans["status"] == TransactionType.FAILED.value:
                        resultResponse["code"] = "failure"
                        resultResponse["message"] = "Your balance does  not have enough money to confirm this " \
                                                    "transaction"
                        self.send_response(400, "failure")
                    else:
                        resultResponse["code"] = "success"
                        resultResponse["message"] = "Transaction '" + jsonObj["transactionId"] + "' is confirmed " \
                                                                                             "successfully."
                        self.send_response(200)
                else:
                    resultResponse["code"] = "failure"
                    resultResponse["message"] = "Fail to confirm transaction '" + jsonObj["transactionId"] + "'."
                    self.send_response(400, "failure")
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            responseStr = json.dumps(resultResponse)
            self.wfile.write(responseStr.encode(encoding='utf_8'))
        elif re.search('/transaction/verify/*', self.path):
            resultResponse = {
                "code": "",
                "message": ""
            }
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                jwtStr = self.headers.get('Authentication')
                newTrans = TransactionService.verifyTransaction(jwtStr, jsonObj["transactionId"])
                if newTrans is not None:
                    if newTrans["status"] == TransactionType.FAILED.value:
                        resultResponse["code"] = "failure"
                        resultResponse["message"] = "Your balance does  not have enough money to verify this " \
                                                    "transaction"
                        self.send_response(400, "failure")
                    else:
                        self.send_response(200)
                        resultResponse["code"] = "success"
                        resultResponse["message"] = "Transaction '" + jsonObj["transactionId"] + "' is verified " \
                                                                                                 "successfully."
                else:
                    resultResponse["code"] = "failure"
                    resultResponse["message"] = "Fail to verify transaction '" + jsonObj["transactionId"] + "'."
                    self.send_response(400, "failure")
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            responseStr = json.dumps(resultResponse)
            self.wfile.write(responseStr.encode(encoding='utf_8'))
        elif re.search('/transaction/cancel/*', self.path):
            resultResponse = {
                "code": "",
                "message": ""
            }
            if self.headers.get('content-type') == 'application/json':
                jsonObj = CommonUtils.extractJsonStr(self)
                jwtStr = self.headers.get('Authentication')
                newTrans = TransactionService.cancelTransaction(jwtStr, jsonObj["transactionId"])
                if newTrans is not None:
                    resultResponse["code"] = "success"
                    resultResponse["message"] = "Transaction '" + jsonObj["transactionId"] + "' is canceled " \
                                                                                             "successfully."
                    self.send_response(200)
                else:
                    resultResponse["code"] = "failure"
                    resultResponse["message"] = "Fail to cancel transaction '" + jsonObj["transactionId"] + "'."
                    self.send_response(400, "failure")
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            responseStr = json.dumps(resultResponse)
            self.wfile.write(responseStr.encode(encoding='utf_8'))
