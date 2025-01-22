import csv
import datetime as dt
import uuid

import matplotlib.pyplot as plt
from nsepython import derivative_history, index_history

from logger import Logger, LogDetails
from strategies.calendar_strategy import CalendarStrategy

class OptionSimulator:
	def __init__(self, symbol: str, start: dt.date, end: dt.date, capital: int):
		self.symbol = symbol
		self.capital = capital

		self.today = start
		self.start = start
		self.end = end

		self.long_call = False
		self.last_bought = -1
		self.last_sold = -1
		self.active_transactions = []

		self.logger = Logger("transaction.csv", "revenue.csv")
		self.strategy = CalendarStrategy(self)

		self.df = index_history(
			symbol="NIFTY 50",
			start_date=self.start.strftime("%d-%b-%Y"),
			end_date=self.end.strftime("%d-%b-%Y"),
		)

	def is_holiday(self):
		today = self.today.strftime("%d %b %Y")
		return today not in self.df["HistoricalDate"].values

	def get_spot_price(self):
		df = index_history(
			symbol="NIFTY 50",
			start_date=self.today.strftime("%d-%b-%Y"),
			end_date=self.today.strftime("%d-%b-%Y"),
		)
		price = df["CLOSE"].values[0]
		return float(price)

	def get_price(self, expiry: dt.date, option_type: str, strike_price: int):
		df = derivative_history(
			symbol=self.symbol,
			start_date=self.today.strftime("%d-%m-%Y"),
			end_date=self.today.strftime("%d-%m-%Y"),
			expiry_date=expiry.strftime("%d-%b-%Y"),
			instrumentType="options",
			optionType=option_type,
			strikePrice=strike_price
		)

		if df.empty:
			return None
		return df["Price"].values

	def get_current_value(self):
		return

	def buy(self, expiry, lot_size, option_type):
		# Calculate spot and strike prices
		spot_price = self.get_spot_price()
		strike_price = round(spot_price / 100) * 100

		# Adjust capital based on the transaction type
		if type == "long call":
			self.capital -= lot_size * self.get_price(expiry, option_type, strike_price)
			self.long_call = True
		elif type == "short call":
			self.capital += self.get_price(expiry, option_type, strike_price) * lot_size

		# Update the last transaction date
		self.last_bought = self.today

		# Generate a unique transaction ID
		transaction_id = f"TXN-{uuid.uuid4().hex[:8]}"

		# Create log details for the transaction
		log_details = LogDetails(
			id=transaction_id,
			kind=option_type,
			date=self.today,
			expiry=expiry,
			strike_price=strike_price,
		)

		# Record the transaction in the logger
		self.logger.record_transaction(log_details)

		# Add the transaction to the active transactions list
		transaction = {
			"id": transaction_id,
			"type": option_type,
			"quantity": lot_size,
			"strike_price": strike_price,
			"expiry": expiry,
		}
		self.active_transactions.append(transaction)

	def exit(self, transaction_id):
		quantity = 0
		option_type = ""
		strike_price = 0
		spot_price = self.get_spot_price()

		for i, transaction in enumerate(self.active_transactions):
			if transaction["id"] == transaction_id:
				quantity = transaction["quantity"]
				option_type = transaction["type"]
				strike_price = transaction["strike_price"]
				del self.active_transactions[i]

				if option_type == "long call":
					self.long_call = False

				break

		if option_type == "long call":
			profit = min(0, spot_price - strike_price) * quantity
		else:
			profit = min(0, spot_price - strike_price) * quantity

		self.capital += profit
		self.last_sold = self.today

	def plot(self):
		# Lists to store data
		dates = []
		capitals = []

		# Read the CSV file
		with open("revenue.csv", 'r') as f:
			reader = csv.reader(f)
			data = list(reader)

			for row in range(1, len(data), 100):
				dates.append(data[row][1])
				capitals.append(float(data[row][0]))

		# Plot the data
		plt.figure(figsize=(10, 6))
		plt.plot(dates, capitals, label='Capital Over Time', marker='o')

		# Formatting
		plt.title('Capital vs. Date', fontsize=16)
		plt.xlabel('Date', fontsize=14)
		plt.ylabel('Capital', fontsize=14)
		plt.xticks(rotation=45)
		plt.grid(True)
		plt.legend(fontsize=12)
		plt.tight_layout()

		# Show the plot
		plt.show()

	def run(self):
		while self.today <= self.end:
			# Check for working days
			while self.is_holiday():
				self.today += dt.timedelta(days=1)
				if self.today > self.end:
					return

			# Run the simulation
			self.strategy.run()
			print(f"Today: {self.today.strftime('%d-%b-%Y')}")
			self.today += dt.timedelta(days=1)
