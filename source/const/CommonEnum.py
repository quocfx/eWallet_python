from enum import Enum


class AccountTypes(Enum):
    PERSONAL = "PERSONAL"
    MERCHANT = "MERCHANT"
    ISSUER = "ISSUER"


class TransactionType(Enum):
    INITIALIZED = 'INITIALIZED'
    CONFIRMED = 'CONFIRMED'
    VERIFIED = 'VERIFIED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    EXPIRED = 'EXPIRED'
    FAILED = 'FAILED'
