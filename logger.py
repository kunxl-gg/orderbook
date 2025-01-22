import csv
import datetime as dt
from dataclasses import dataclass

@dataclass
class LogDetails:
    id: int
    kind: str
    date: dt.date
    expiry: dt.date
    strike_price: float

class Logger:
    def __init__(self, file_path, log_file):
        self.file_path = file_path
        self.log_file = log_file

        with open(self.file_path, "w", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "type", "strike_price", "expiry"])

        with open(self.log_file, 'w', newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(["capital", "date"])

    def record_transaction(self, log: LogDetails):
        with open(self.file_path, "a", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow([log.id, log.kind, log.date, log.expiry, log.strike_price])

    def record_revenue(self, revenue, date):
        with open(self.log_file, "a", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow([revenue, date])
