from pysondb import getDb

accountDbPath = 'db/account.json'


def saveAccount(newAccount):
    accountDb = getDb(accountDbPath)
    updatedAccount = {
        "accountId": newAccount["accountId"],
        "accountName": newAccount["accountName"],
        "accountType": newAccount["accountType"],
        "balance": newAccount["balance"],
        "url": newAccount["url"]
    }
    accountDb.add(updatedAccount)
    return newAccount


def updateById(updatedAcc):
    accountDb = getDb(accountDbPath)
    accountDb.updateById(updatedAcc["id"], updatedAcc)
    return updatedAcc


def getAccountByAccId(accId):
    accountDb = getDb(accountDbPath)
    return accountDb.getByQuery(query={
        "accountId": accId
    })


def getAccountByAccIdAndAccType(accId, accType):
    accountDb = getDb(accountDbPath)
    return accountDb.getByQuery(query={
        "accountId": accId,
        "accountType": accType
    })
