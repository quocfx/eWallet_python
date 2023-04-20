from pysondb import getDb
from uuid import uuid4

def addNewMerchant(merchantName, merchantUrl):
    merchantDb = getDb('db/merchant.json')
    accountId = str(uuid4())
    merchantId = str(uuid4())
    apiKey =  str(uuid4())
    newMerchant = {
        "accountId": accountId,
        "merchantId": merchantId,
        "merchantName": merchantName,
        "merchantUrl": merchantUrl,
        "apiKey": apiKey
    }
    merchantDb.add(newMerchant)
    return newMerchant
