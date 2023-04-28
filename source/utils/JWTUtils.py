import jwt
from datetime import datetime, timedelta

secretKey = "account_s3cr3t"
tokenExpTime = 3600  # in seconds
jwtAlgo = "HS256"
import time


def generateJWTFromAccount(accId):
    # timeExpired = datetime.now() + timedelta(hours=8)
    # timeExpired = format(timeExpired, '%Y-%m-%d %H:%M:%S')
    timeExpired = int(time.time()) + tokenExpTime
    encoded_jwt = jwt.encode({
        'accountId': accId,
        # 'timeExpired': timeExpired
        'exp': timeExpired
    }, secretKey, algorithm=jwtAlgo)
    return encoded_jwt.encode('utf-8').decode('ascii')
    # return {
    #     "token": encoded_jwt,
    #     "exp": timeExpired
    # }


def verifyToken(token):
    try:
        return jwt.decode(token, secretKey, algorithms=[jwtAlgo])
    except jwt.ExpiredSignatureError:
        # Handle case where token has expired
        return None
    except jwt.InvalidTokenError:
        # Handle case where token is invalid or malformed
        return None


def extractJWT(token):
    return jwt.decode(token, secretKey, algorithms=["HS256"])
