import datetime as dt

from logger import Logger
from simulation import OptionSimulator

if __name__ == "__main__":
	# Config Variables
	symbol = "NIFTY"
	capital = 10000000
	start = dt.date(2022, 1, 1)
	end = dt.date(2025, 1, 1)

	# Initialising the OptionSimulator
	sim = OptionSimulator(symbol=symbol, start=start, end=end, capital=capital)
	sim.run()
	sim.plot()
