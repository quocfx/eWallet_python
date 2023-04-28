from source.utils import (CommonUtils, JWTUtils)
from source.const.CommonEnum import TransactionType
from source.service import AccountService
from source.repository import TransactionRepo
from uuid import uuid4
from datetime import datetime, timedelta


def initTransaction(token, newTransaction):
    account = JWTUtils.verifyToken(token)
    if account is not None:
        account = AccountService.getMerchantAccById(account["accountId"])
        if account is not None:
            currentTime = str(datetime.now())
            newItem = {
                "transactionId": str(uuid4()),
                "merchantId": account["accountId"],
                "incomeAccount": account["accountId"],
                "outcomeAccount": None,
                "amount": newTransaction["amount"],
                "extraData": newTransaction["extraData"],
                "signature": newTransaction["signature"],
                "status": TransactionType.INITIALIZED.value,
                "createdDate": currentTime,
                "updateDate": currentTime
            }
            return TransactionRepo.saveTransaction(newItem)
    return None


def confirmTransaction(token, transactionId):
    account = JWTUtils.verifyToken(token)
    if account is not None:
        account = AccountService.getPersonalAccById(account["accountId"])
        if account is not None:
            transaction = TransactionRepo.getTransByTransId(transactionId)
            if transaction is not None and transaction["status"] == TransactionType.INITIALIZED.value:
                transaction["updateDate"] = str(datetime.now())
                if account["balance"] > transaction["amount"]:
                    transaction["outcomeAccount"] = account["accountId"]
                    transaction["status"] = TransactionType.CONFIRMED.value
                else:
                    transaction["status"] = TransactionType.FAILED.value
                return TransactionRepo.updateById(transaction)
    return None


def verifyTransaction(token, transactionId):
    account = JWTUtils.verifyToken(token)
    if account is not None:
        account = AccountService.getPersonalAccById(account["accountId"])
        if account is not None:
            transaction = TransactionRepo.getTransByTransId(transactionId)
            if transaction is not None and transaction["status"] == TransactionType.CONFIRMED.value:
                if account["balance"] >= transaction["amount"]:
                    transaction["updateDate"] = str(datetime.now())
                    transaction["status"] = TransactionType.VERIFIED.value
                    transactionResult = TransactionRepo.updateById(transaction)
                    if transactionResult is not None:
                        merchant = AccountService.getMerchantAccById(transaction["merchantId"])
                        if merchant is not None:
                            # Need to be in  transaction or promise all?
                            account["balance"] = float(account["balance"]) - float(transaction["amount"])
                            merchant["balance"] = float(merchant["balance"]) + float(transaction["amount"])
                            AccountService.updateById(account)
                            AccountService.updateById(merchant)
                            transaction["updateDate"] = str(datetime.now())
                            transaction["status"] = TransactionType.COMPLETED.value
                            return TransactionRepo.updateById(transaction)
                else:
                    transaction["updateDate"] = str(datetime.now())
                    transaction["status"] = TransactionType.FAILED.value
                    return TransactionRepo.updateById(transaction)
    return None


def cancelTransaction(token, transactionId):
    account = JWTUtils.verifyToken(token)
    if account is not None:
        account = AccountService.getPersonalAccById(account["accountId"])
        if account is not None:
            currentTime = str(datetime.now())
            transaction = TransactionRepo.getTransByTransId(transactionId)
            if transaction is not None and (transaction["status"] == TransactionType.INITIALIZED.value or
                    transaction["status"] == TransactionType.CONFIRMED.value):
                transaction["updateDate"] = currentTime
                transaction["status"] = TransactionType.CANCELED.value
                return TransactionRepo.updateById(transaction)
    return None


def expireTransaction():
    listTransaction = TransactionRepo.getTransByStatus([TransactionType.INITIALIZED.value,
                                                        TransactionType.CONFIRMED.value,
                                                        TransactionType.VERIFIED.value])
    resultList = []
    for transaction in listTransaction:
        createdTimeTransaction = datetime.strptime(transaction["createdDate"], '%Y-%m-%d %H:%M:%S.%f')
        expiredTime = createdTimeTransaction + timedelta(minutes=5)
        if datetime.now() > expiredTime:
            transaction["status"] = TransactionType.EXPIRED.value
            transaction["updateDate"] = str(datetime.now())
            TransactionRepo.updateById(transaction)
            resultList.append(transaction["transactionId"])
    print("Expire following transaction:")
    print(resultList)
    return resultList
