import csv
import datetime as dt

class Logger:
	def __init__(self, file_path):
		self.file_path = file_path

		with open(self.file_path, 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["id", "type", "strike_price", "expiry"])

	def record_transaction(self, transaction_id, type, strike_price, expiry):
		with open(self.file_path, 'a', newline='') as f:
			writer = csv.writer(f)
			writer.writerow([transaction_id, type, strike_price, expiry])
