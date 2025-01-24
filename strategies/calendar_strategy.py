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

		if last_sold == -1:
			return False

		if len(self.simulator.expiries) == 0:
			return False

		expiry = self.simulator.expiries[0]
		if dt.datetime.strptime(expiry, "%d-%b-%Y").date() > self.simulator.end:
			return False

		# Buy on the first day after having sold an option
		if last_sold.isoformat() > last_bought.isoformat():
			return True

		return False

	def run(self):
		# Get number of days to the next Thursday
		should_buy = self.should_buy()

		# Buy a long call if you don't have any
		if should_buy and not self.simulator.long_call:
			target_month = dt.datetime.strptime(self.simulator.expiries[0], "%d-%b-%Y").date().month
			print(target_month)
			for e in self.simulator.expiries:
				if dt.datetime.strptime(e, "%d-%b-%Y").date().month == target_month:
					exp = e
				else:
					break
			expiry = dt.datetime.strptime(exp, "%d-%b-%Y").date()
			print(type(expiry), expiry.strftime("%d-%b-%Y"))
			self.simulator.enter(expiry, 75, "long call")

		# Buy a short call
		elif should_buy:
			expiry = dt.datetime.strptime(self.simulator.expiries[0], "%d-%b-%Y").date()
			self.simulator.enter(expiry, 75, "short call")

			# Remove the expiry date
			self.simulator.expiries.pop(0)

		# Check for expired options
		for transaction in self.simulator.active_transactions:
			if self.simulator.today >= transaction["expiry"]:
				self.simulator.exit(transaction["id"])
