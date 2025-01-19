import csv
import datetime as dt
import matplotlib.pyplot as plt
import logging
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

        self.logger = Logger("transaction.csv", "revenue.csv")
        self.strategy = Strategy(self, 0.01, 0.05)

        nifty = yf.download(self.symbol, self.start, self.end)
        if nifty is None or nifty.empty:
            raise ValueError(f"No data for {self.symbol} from {self.start} to {self.end}.")

        self.data = nifty

    def is_holiday(self):
        return self.today.strftime("%Y-%m-%d %H:%M:%S") not in self.data.index

    def get_price(self):
        price = self.data.loc[self.today.strftime("%Y-%m-%d %H:%M:%S"), "Close"]
        return float(price.squeeze())

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
        spot_price = self.get_price()
        strike_price = round(spot_price / 10) * 10

        if type == "long call":
            self.capital -= lot_size * self.strategy.get_premium(type)
            self.long_call = True
        elif type == "short call":
            self.capital += self.strategy.get_premium(type) * lot_size

        self.last_transaction = self.today

        # Record the transaction.
        transaction_id = f"TXN-{uuid.uuid4().hex[:8]}"
        self.logger.record_transaction(transaction_id, self.today, type, strike_price, expiry)

        transaction = {
            "id": transaction_id,
            "type": type,
            "quantity": lot_size,
            "strike_price": strike_price,
            "expiry": expiry,
        }
        self.active_transactions.append(transaction)

    def exit(self, type, transaction_id):
        spot_price = self.get_price()

        for i, transaction in enumerate(self.active_transactions):
            if transaction["id"] == transaction_id:
                quantity = transaction["quantity"]
                strike_price = transaction["strike_price"]
                del self.active_transactions[i]

                if transaction["type"] == "long call":
                    self.long_call = False

                break

        if type == "long call":
            profit = min(0, spot_price - strike_price) * quantity
        elif type == "short call":
            profit = min(0, spot_price - strike_price) * quantity
        elif type == "long put":
            profit = min(0, strike_price - spot_price) * quantity
        elif type == "short put":
            profit = min(0, strike_price - spot_price) * quantity


        self.capital += profit

    def plot(self):
        # Lists to store data
        dates = []
        capitals = []

        # Read the CSV file
        with open("revenue.csv", 'r') as f:
            reader = csv.reader(f)
            data = list(reader)

            for row in range(1, len(data), 100):
                dates.append(data[row][1])
                capitals.append(float(data[row][0]))

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(dates, capitals, label='Capital Over Time', marker='o')

        # Formatting
        plt.title('Capital vs. Date', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Capital', fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend(fontsize=12)
        plt.tight_layout()

        # Show the plot
        plt.show()

    def run(self):
        while self.today <= self.end:
            # Check for working days
            while self.is_holiday():
                self.today += dt.timedelta(days=1)
                if self.today > self.end:
                    return

            # Run the simulation
            self.strategy.run()
            print(f"Current Portfolio Size: {self.get_current_value():.2f} as of {self.today.strftime('%Y-%m-%d')}")
            self.logger.record_revenue(self.get_current_value(), self.today.strftime('%Y-%m-%d'))

            self.today += dt.timedelta(days=1)
