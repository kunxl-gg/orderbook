import datetime as dt
import uuid

class Strategy:
	def __init__(self, simulator, premium, margin):
		self.simulator = simulator
		self.premium = premium
		self.margin = margin

	def is_expired(self, transaction):
		return self.simulator.today >= transaction["expiry"]

	def run(self):
		if self.simulator.today.weekday() == 4:
			# Get the current spot price to determine the strike price
			spot_price = self.simulator.get_price()
			strike_price = round(spot_price / 10) * 10  # Round to nearest 10 for strike price

			# Buy long call expiring 1 month from now
			long_call_expiry = self.simulator.today + dt.timedelta(weeks=4)  # Expire in 4 weeks
			self.buy_long_call(strike_price, long_call_expiry)

			# Sell short call expiring in 1 week
			short_call_expiry = self.simulator.today + dt.timedelta(weeks=1)  # Expire in 1 week
			self.sell_short_call(strike_price, short_call_expiry)

		# Move to the next day
		self.simulator.today += dt.timedelta(days=1)

		# Check for expired options
		for transaction in self.transactions:
			if self.is_expired(transaction):
				print(f"Option with ID {transaction['id']} has expired.")
				# Optional: handle expired option logic (e.g., close position, etc.)
