from abc import ABC, abstractmethod

class Strategy(ABC):
	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def should_buy(self):
		pass
	
	@abstractmethod
	def run(self):
		pass
