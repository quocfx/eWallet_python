from pysondb import getDb
from datetime import datetime

transactionDbPath = 'db/transaction.json'


def saveTransaction(newTransaction):
    transactionDb = getDb(transactionDbPath)
    updatedTransaction = {
        "transactionId": newTransaction["transactionId"],
        "merchantId": newTransaction["merchantId"],
        "incomeAccount": newTransaction["incomeAccount"],
        "outcomeAccount": newTransaction["outcomeAccount"],
        "amount": newTransaction["amount"],
        "extraData": newTransaction["extraData"],
        "signature": newTransaction["signature"],
        "status": newTransaction["status"],
        "createdDate": newTransaction["createdDate"],
        "updateDate": newTransaction["updateDate"]
    }
    transactionDb.add(updatedTransaction)
    return updatedTransaction


def updateById(updatedTrans):
    transactionDb = getDb(transactionDbPath)
    transactionDb.updateById(updatedTrans["id"], updatedTrans)
    return updatedTrans


def getTransByTransId(transId):
    transactionDb = getDb(transactionDbPath)
    result = transactionDb.getByQuery(query={
        "transactionId": transId
    })
    if result is not None and len(result) > 0:
        return result[0]
    else:
        return None


def getTransByStatus(statusList):
    transactionDb = getDb(transactionDbPath)
    allTransactions = transactionDb.getAll()
    return [transaction for transaction in allTransactions if transaction["status"] in statusList]
