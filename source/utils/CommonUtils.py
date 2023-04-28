import json
from source.const.CommonEnum import AccountTypes
from datetime import datetime, timedelta


def extractJsonStr(self):
    length = int(self.headers.get('content-length'))
    bodyStr = self.rfile.read(length).decode('utf8')
    return json.loads(bodyStr)


def extractPathVariable(source, startStr, endStr):
    startIndex = source.index(startStr)
    if startIndex < 0:
        return ""
    endIndex = source.index(endStr)
    if endIndex < 0:
        return ""
    return source[startIndex + len(startStr): endIndex]


def checkAccountTypes(accountType):
    myTypes = [accType.value for accType in AccountTypes]
    return accountType.upper() in myTypes


def checkTimeExpired(source):
    date_obj = datetime.strptime(source, '%Y-%m-%d %H:%M:%S')
    return datetime.now() > date_obj
