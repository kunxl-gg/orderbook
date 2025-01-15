import os
import json
import datetime as dt

class Logger:
	def __init__(self, file_path):
		self.file_path = file_path

		with open(self.transaction_log, 'w') as f:
			json.dump([], f)

	def _load_transactions(self):
		with open(self.file_path, 'r') as f:
			return json.load(f)

	def _save_transactions(self, transactions):
		with open(self.file_path, 'w') as f:
			json.dump(transactions, f, indent=4)

	def record_transaction(self, transaction_id, type, strike_price, expiry):
		transactions = self._load_transactions()

		transactions.append({"id": transaction_id, "expiry": expiry.isoformat()})
		self._save_transactions(transactions)

	def read_transactions(self):
		return self._load_transactions()
