import datetime as dt

from strategy import Strategy

class CalendarStrategy(Strategy):
	def __init__(self, simulator):
		self.simulator = simulator

	def should_buy(self):
		last_sold = self.simulator.last_sold
		last_bought = self.simulator.last_bought

		if last_bought == -1:
			return True

		if last_sold:
			return False

		# Buy on the first day after having sold an option
		if last_sold.isoformat() > last_bought.isoformat():
			return True

		return False

	def run(self):
		# Check for expired options
		for transaction in self.simulator.active_transactions:
			if self.simulator.today >= transaction["expiry"]:
				self.simulator.exit(transaction["id"])

		# Get number of days to the next Thursday
		days_ahead = (3 - self.simulator.today.weekday() + 7) % 7
		days_ahead = days_ahead or 7

		# Buy a short call
		if self.should_buy():
			expiry = self.simulator.today + dt.timedelta(days=days_ahead)
			self.simulator.buy(expiry, 10, "short call")

		# Buy a long call if you don't have any
		if self.should_buy() and not self.simulator.long_call:
			days_ahead = days_ahead + 3 * 7
			expiry = self.simulator.today + dt.timedelta(days=days_ahead)

			self.simulator.buy(expiry, 10, "long call")
