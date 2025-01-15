import datetime as dt
import pandas as pd
import yfinance as yf

from strategy import Strategy

class OptionSimulator:
	def __init__(self, symbol: str, start: dt, end: dt, capital: int):
		self.capital = capital
		self.investment = 0
		self.start = start
		self.today = start
		self.end = end
		self.stock = symbol
		self.strategy = Strategy()

		self.fetch_data()

	def fetch_data(self):
		nifty = yf.download(self.stock, self.start, self.end)
		if nifty is None or nifty.empty:
			raise ValueError(f"No data for {self.symbol} from {self.start} to {self.end}.")

		self.data = yf.download(self.stock, self.start, self.end)

	def get_price(self):
		return self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]

	def make_transaction(self):
		pass

	def is_holiday(self):
		return self.today.strftime("%Y-%m-%d %H:%M:%S") not in self.data.index

	def get_current_value(self):
		pass

	def buy(self, date, allocated_money):
		spot_price = self.df.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]
		strike_price = round(spot_price / 10) * 10
		quantity = allocated_money / strike_price
		self.capital -= quantity * self.strategy.premium
		# Make a transaction

	def sell(self):
		if (self.today.weekday() == 3):
			# We sell only on thursdays of a week.
			pass

	def run(self):
		while self.today <= self.end:
			while self.is_holiday():
				self.today += dt.timedelta(days=1)
			# Run the simulation

			self.today += dt.timedelta(days=7)


	def plot(self):
		pass
