from pysondb import getDb
from uuid import uuid4
from source.repository.AccountRepo import (saveAccount)
from source.const.CommonEnum import AccountTypes


def addNewMerchant(merchantName, merchantUrl):
    accountId = str(uuid4())
    accountType = AccountTypes.MERCHANT.value
    newMerchant = {
        "accountId": accountId,
        "accountType": accountType,
        "accountName": merchantName,
        "url": merchantUrl,
        "balance": 0
    }
    saveAccount(newMerchant)
    return newMerchant