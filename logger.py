import csv
import datetime as dt
from dataclasses import dataclass

@dataclass
class LogDetails:
    id: str
    kind: str
    date: dt.date
    expiry: dt.date
    strike_price: float
    price: float

class Logger:
    def __init__(self, transactions, revenue):
        self.transactions = transactions
        self.revenue = revenue

        with open(self.transactions, "w", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "type", "date", "expiry", "strike_price", "premium"])

        with open(self.revenue, 'w', newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(["capital", "date"])

    def record_transaction(self, log: LogDetails):
        with open(self.transactions, "a", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow([log.id, log.kind, log.date, log.expiry, log.strike_price, log.price])

    def record_revenue(self, revenue, date):
        with open(self.revenue, "a", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow([revenue, date])
