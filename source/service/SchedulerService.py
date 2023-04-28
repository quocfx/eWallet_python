from apscheduler.schedulers.blocking import BlockingScheduler
from source.service.TransactionService import expireTransaction


def cleanupExpiredTransaction():
    expireTransaction()


def startJob():
    scheduler = BlockingScheduler()
    # Run the schedule per 5 mins
    scheduler.add_job(cleanupExpiredTransaction, 'interval', seconds=300)
    scheduler.start()
