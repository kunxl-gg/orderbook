import datetime as dt
import uuid

from simulation import OptionSimulator

class Strategy:
	def __init__(self, simulator: OptionSimulator, premium, margin):
		self.simulator = simulator
		self.premium = premium
		self.margin = margin

	def get_premium(self, type) -> int:
		if type == "long call":
			return 4 * self.premium * self.simulator.get_price()
		else:
			return self.premium * self.simulator.get_price()


	def is_expired(self, transaction):
		return self.simulator.today >= transaction["expiry"]

	def should_buy(self):
		today = self.simulator.today
		last_transaction = self.simulator.last_transaction

		current_week = self.simulator.today.isocalendar().week
		last_week = last_transaction.isocalendar().week

		if current_week == last_week:
			return False
		if today.isoformat() < last_transaction.isoformat():
			return False

		return True

	def run(self):
		# Check for expired options
		for transaction in self.simulator.active_transactions:
			if self.simulator.today >= transaction["expiry"]:
				self.simulator.exit(transaction["type"], transaction["id"])

		days_ahead = (3 - self.simulator.today.weekday() + 7) % 7
		days_ahead = days_ahead or 7

		if self.should_buy():
			expiry = self.simulator.today + dt.timedelta(days=days_ahead)
			self.simulator.buy("short call", expiry, 10)

		if not self.simulator.long_call:
			days_ahead = days_ahead + 3 * 7
			expiry = self.simulator.today + dt.timedelta(days=days_ahead)

			self.simulator.buy("long call", expiry, 10)
