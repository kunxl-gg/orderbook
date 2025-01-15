import os
import json
from datetime import datetime

class Logger:
    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _load_transactions(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _save_transactions(self, transactions):
        with open(self.file_path, 'w') as f:
            json.dump(transactions, f, indent=4)

    def record_transaction(self, transaction_id, expiry):
        transactions = self._load_transactions()

        transactions.append({"id": transaction_id, "expiry": expiry})

        transactions.sort(key=lambda x: datetime.fromisoformat(x['expiry']))

        self._save_transactions(transactions)

    def first_transaction(self):
        transactions = self._load_transactions()

        if transactions:
            return transactions[0]
        else:
            print("No transactions available.")

    def read_transactions(self):
        return self._load_transactions()

    def clear_transactions(self):
        self._save_transactions([])

