from pysondb import getDb
from uuid import uuid4
import jwt
from datetime import datetime, timedelta
from source.utils import (CommonUtils, JWTUtils)
from source.const.CommonEnum import AccountTypes
from source.repository.AccountRepo import (saveAccount, getAccountByAccId, updateById, getAccountByAccIdAndAccType)
import decimal


def addNewAccount(newAccount):
    newAccount['accountId'] = str(uuid4())
    newAccount['balance'] = 0
    newAccount['url'] = ""
    return saveAccount(newAccount)


def getAccById(accId):
    return getAccountByAccId(accId)


def getMerchantAccById(accId):
    merchantAcc = getAccountByAccIdAndAccType(accId, AccountTypes.MERCHANT.value)
    if merchantAcc is not None and len(merchantAcc) > 0:
        return merchantAcc[0]
    else:
        return None


def getPersonalAccById(accId):
    personalAcc = getAccountByAccIdAndAccType(accId, AccountTypes.PERSONAL.value)
    if personalAcc is not None and len(personalAcc) > 0:
        return personalAcc[0]
    else:
        return None


def topupAccount(token, accId, amount):
    # check the token is the issue banking
    decoded_token = JWTUtils.verifyToken(token)
    print(decoded_token)
    if decoded_token is not None:
        issuerAcc = getAccountByAccId(decoded_token["accountId"])
        # Ensure the token is from Issuer account
        if issuerAcc is not None and len(issuerAcc) > 0 and issuerAcc[0]["accountType"] == "ISSUER":
            topupAcc = getAccountByAccId(accId)
            if topupAcc is not None and len(topupAcc) > 0:
                topupAcc = topupAcc[0]
                topupAcc['balance'] = float(decimal.Decimal(topupAcc['balance']) + decimal.Decimal(amount))
                print("topupAcc:", topupAcc)
                return updateById(topupAcc)
    return None
