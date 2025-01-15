import datetime as dt
import numpy as np
import pandas as pd
import yfinance as yf

from logger import Logger
from simulation import OptionSimulator

if __name__ == "__main__":
	# Declare all the config variables
	symbol = "^NSEI"
	capital = 10000000
	today = dt.date(2022, 1, 3)
	last_day = dt.date(2025, 1, 1)

	# Initialise the OptionSimulator Object
	sim = OptionSimulator(symbol, today, today + dt.timedelta(days=7), capital)
	sim.logger.record_transaction(1, today + dt.timedelta(days=4))
	sim.run()
