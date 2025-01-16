import csv
import datetime as dt

class Logger:
	def __init__(self, file_path, log_file):
		self.file_path = file_path
		self.log_file = log_file

		with open(self.file_path, 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["id", "date", "type", "strike_price", "expiry"])

		with open(self.log_file, 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["capital", "date"])

	def record_transaction(self, transaction_id, date, type, strike_price, expiry):
		with open(self.file_path, 'a', newline='') as f:
			writer = csv.writer(f)
			writer.writerow([transaction_id, date, type, strike_price, expiry])


	def record_revenue(self, revenue, date):
		with open(self.log_file, 'a', newline='') as f:
			writer = csv.writer(f)
			writer.writerow([revenue, date])
