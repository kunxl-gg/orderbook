import os
import json
import datetime as dt

class Logger:
	def __init__(self, active_path, transaction_path):
		self.active_log = active_path
		self.transaction_log = transaction_path

		with open(self.active_log, 'w') as f:
			json.dump([], f)

		with open(self.transaction_log, 'w') as f:
			json.dump([], f)


	def _load_transactions(self):
		with open(self.transaction_log, 'r') as f:
			return json.load(f)

	def _save_transactions(self, transactions):
		with open(self.transaction_log, 'w') as f:
			json.dump(transactions, f, indent=4)

	def record_transaction(self, transaction_id, type, strike_price, expiry):
		transactions = self._load_transactions()

		# Append the new transaction
		transactions.append({"id": transaction_id, "expiry": expiry.isoformat()})

		# Sort transactions by the 'expiry' date
		transactions.sort(key=lambda x: x['expiry'])

		# Save the updated transactions
		self._save_transactions(transactions)


	def first_transaction(self):
		transactions = self._load_transactions()

		if transactions:
			return transactions[0]
		else:
			print("No transactions available.")
			return None

	def read_transactions(self):
		return self._load_transactions()
