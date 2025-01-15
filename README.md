# Options Trading Simulator

A simulator for testing and analyzing options trading strategies, focusing on the **Calendar Spread Strategy**.

## Features
- Simulate options trading with realistic market conditions.
- Built-in logging to track trades and market activity.
- Modular design for easy integration of custom strategies.
- Pre-implemented **Calendar Spread Strategy**.

## Project Structure
- **`Simulation`**: Core logic for simulating options trading.
- **`Logger`**: Handles logging of simulation events, trades, and results.
- **`Strategy`**: Implements the **Calendar Spread Strategy**, with flexibility to extend or modify for other strategies.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kunxl-gg/orderbook/
   ```
2. Navigate to the project directory:
   ```bash
	cd orderbook
   ```
1. Install dependencies (if applicable):
   ```bash
	pip install -r requirements.txt
   ```
2. Run the simulator:
   ```bash
	python main.py
   ```

## Calendar Spread Strategy

The Calendar Spread Strategy involves:

Buying a longer-term option (same strike price).
Selling a shorter-term option of the same underlying asset.
This strategy is typically used to capitalize on differences in time decay (theta) between the two options.
