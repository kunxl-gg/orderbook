import datetime as dt
import pandas as pd
import uuid
import yfinance as yf

from logger import Logger
from strategy import Strategy

class OptionSimulator:
	def __init__(self, symbol: str, start: dt.date, end: dt.date, capital: int):
		self.symbol = symbol
		self.capital = capital

		self.end = end
		self.start = start
		self.today = start

		self.long_call = False
		self.last_transaction = -1
		self.active_transactions = []

		self.logger = Logger("transaction.log")
		self.strategy = Strategy(self, 0.1, 0.5)

		nifty = yf.download(self.symbol, self.start, self.end)
		if nifty is None or nifty.empty:
			raise ValueError(f"No data for {self.symbol} from {self.start} to {self.end}.")

		self.data = nifty

	def is_holiday(self):
		return self.today.strftime("%Y-%m-%d %H:%M:%S") not in self.data.index

	def get_price(self):
		return self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]

	def get_current_value(self):
		value = self.capital
		spot_price = self.get_price()
		for transaction in self.active_transactions:
			if transaction["type"] == "long call":
				value += (spot_price - transaction["strike_price"]) * transaction["quantity"]
			elif transaction["type"] == "short call":
				value += (transaction["strike_price"] - spot_price) * transaction["quantity"]

		return value

	def buy(self, type, expiry, lot_size):
		spot_price = self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]
		strike_price = round(spot_price / 10) * 10

		if type == "long call":
			investment = min(self.capital, lot_size * self.strategy.premium)
			lot_size = investment / self.strategy.get_premium(type)
			self.capital -= lot_size * self.strategy.get_premium(type)
			self.long_call = True
		elif type == "short call":
			self.capital += self.strategy.get_premium() * lot_size

		self.last_transaction = self.today

		transaction = {
			"id": transaction_id,
			"type": type,
			"strike_price": strike_price,
			"expiry": expiry,
		}
		self.active_transactions.append(transaction)

		# Record the transaction.
		transaction_id = f"TXN-{uuid.uuid4().hex[:8]}"
		self.logger.record_transaction(transaction_id, type, strike_price, expiry)

	def exit(self, type, transaction_id):
		spot_price = self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]

		for i, transaction in enumerate(self.active_transactions):
			if transaction["id"] == transaction_id:
				quantity = transaction["quantity"]
				strike_price = transaction["strike_price"]
				del self.active_transactions[i]

				if transaction["type"] == "long call":
					self.long_call = False

				break

		# Here you can make the different P&L calculations
		if type == "long call":
			profit = max(0, spot_price - strike_price) * quantity
		elif type == "short call":
			profit = max(0, spot_price - strike_price) * quantity
		elif type == "long put":
			profit = max(0, strike_price - spot_price) * quantity
		elif type == "short put":
			profit = max(0, strike_price - spot_price) * quantity

		self.capital += profit

		# Record the transaction.
		transaction_id = f"TXN-{uuid.uuid4().hex[:8]}"
		self.logger.record_transaction(transaction_id, type, strike_price, self.today)

	def run(self):
		while self.today <= self.end:
			# Check for working days
			while self.is_holiday():
				self.today += dt.timedelta(days=1)

			# Run the simulation
			self.strategy.run()
			print(f"Current Portfolio Size: ${self.get_current_value():,.2f}\
		 			as of {self.today.strftime('%B %d, %Y')}")

			self.today += dt.timedelta(days=1)
