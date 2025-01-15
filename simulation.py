import datetime as dt
import pandas as pd
import uuid
import yfinance as yf

from logger import Logger
from strategy import Strategy

class OptionSimulator:
	def __init__(self, symbol: str, start: dt.date, end: dt.date, capital: int):
		self.initial_capital = capital
		self.capital = capital
		self.start = start
		self.today = start
		self.end = end
		self.symbol = symbol
		self.logger = Logger("active.json", "transaction.json")
		self.strategy = Strategy(self, 0, 0)
		self.fetch_data()

	def fetch_data(self):
		nifty = yf.download(self.symbol, self.start, self.end)
		if nifty is None or nifty.empty:
			raise ValueError(f"No data for {self.symbol} from {self.start} to {self.end}.")

		self.data = yf.download(self.symbol, self.start, self.end)

	def get_price(self):
		return self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]

	def is_holiday(self):
		return self.today.strftime("%Y-%m-%d %H:%M:%S") not in self.data.index

	def buy(self, type, expiry, lot_size):
		spot_price = self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]
		strike_price = round(spot_price / 10) * 10

		if type == "long call" or type == "long put":
			investment = min(self.initial_captial, lot_size * self.strategy.premium)
			lot_size = investment / self.strategy.premium
			self.capital -= lot_size * self.strategy.premium
		elif type == "short call" or type == "short put":
			self.capital -= self.strategy.margin

		# Record the transaction.
		transaction_id = f"{"TXN"}-{uuid.uuid4().hex[:8]}"
		self.logger.record_transaction(transaction_id, type, strike_price, expiry)

	def exit(self, type, transaction_id):
		spot_price = self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]
		strike_price = 1
		premium = 1
		quantity = 1

		# Here you can make the different P&L calculations
		if type == "long call":
			profit = max(0, spot_price - strike_price) * quantity
		elif type == "short call":
			profit = max(0, spot_price - strike_price) * quantity
		elif type == "long put":
			profit = (max(0, strike_price - spot_price) - premium) * quantity
		elif type == "short put":
			profit = (premium - max(0, strike_price - spot_price)) * quantity

		self.capital += profit

		# Record the transaction.
		transaction_id = f"{"TXN"}-{uuid.uuid4().hex[:8]}"
		self.logger.record_transaction(transaction_id, type, strike_price, self.today)

	def run(self):
		while self.today <= self.end:
			# Check for working days
			while self.is_holiday():
				self.today += dt.timedelta(days=1)

			# Run the simulation
			self.strategy.run()
			self.today += dt.timedelta(days=1)
