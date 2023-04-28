from http.server import HTTPServer
from source.controller.RouteController import RoutingRequestHandler
from service.SchedulerService import startJob

from threading import Thread
from time import sleep

from source.service import MerchantService
from source.service import TransactionService
import re
import json


def main():
    server = HTTPServer(("localhost", 8080), RoutingRequestHandler)
    print('HTTP Server Running...........')

    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    batch_job_thread = Thread(target=startJob)
    batch_job_thread.daemon = True
    batch_job_thread.start()

    while True:
        sleep(1)


    # server.serve_forever()





if __name__ == '__main__':
    main()
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50SWQiOiIxMzIyMzZhYS0zYmQ2LTQ3NjAtOWU4Mi1hZTM5NWVhYTQxZDAiLCJleHAiOjE2ODI2ODA4MzZ9.IJKsMp4smKcUUymEBq0W2f0I0w9bDCC35aTi3a61XGg"
    # transactionId = "2bf615cb-b4a1-4088-a460-dbf05803e2c1"
    # # # newRequest = {
    # # #     "transactionId": "2bf615cb-b4a1-4088-a460-dbf05803e2c1"
    # # # }
    # newTrans = TransactionService.cancelTransaction(token, transactionId)
    # jsonStr = json.dumps(newTrans)
    # print(jsonStr)
    # from source.repository import TransactionRepo
    # statusList = ["CANCELED", "CONFIRMED"]
    # result = TransactionService.expireTransaction()
    # statusList = ["CANCELED", "INIT", "ACTIVE"]
    # stringTest = "CANCELED"
    # res = stringTest in statusList
    # print(res)
