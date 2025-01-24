from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Abstract base class for implementing different trading strategies.

    This class defines the blueprint for any trading strategy by specifying
    the essential methods that must be implemented by derived classes. These
    include initialization, a decision-making mechanism (`should_buy`), and
    a main execution workflow (`run`).

    Classes inheriting from `Strategy` must override all abstract methods.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the strategy instance.

        This method should be used to set up any required resources,
        variables, or configurations needed by the strategy. Subclasses must
        implement this method to handle their specific initialization logic.
        """
        pass

    @abstractmethod
    def should_buy(self) -> bool:
        """
        Determines whether a buy action should be taken.

        This method should encapsulate the logic for deciding whether the
        current market conditions warrant a buy action. It must return a
        boolean value (`True` to buy, `False` otherwise).
        """
        pass

    @abstractmethod
    def run(self):
        """
        Executes the main workflow of the strategy.

        This method defines the core logic of the trading strategy, including
        processing data, evaluating conditions, and executing trades or other
        actions as necessary.
        """
        pass
