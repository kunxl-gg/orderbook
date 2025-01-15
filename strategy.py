import datetime as dt
import uuid

from simulation import OptionSimulator

class Strategy:
	def __init__(self, simulator: OptionSimulator, premium, margin):
		self.simulator = simulator
		self.premium = premium
		self.margin = margin

	def get_premium(self):
		return self.premium * self.simulator.get_price()

	def is_expired(self, transaction):
		return self.simulator.today >= transaction["expiry"]

	def run(self):
		# Check for expired options
		for transaction in self.simulator.active_transactions:
			if self.simulator.today >= transaction["expiry"]:
				self.simulator.exit(transaction["id"])

		last_week = self.simulator.today.isocalendar()[1]
		current_week = self.simulator.today.isocalendar()[1]

		if last_week == current_week:
			return
		else:
			self.simulator.buy("short call",
					  			self.simulator.today + dt.timedelta(days=7),
								10)
