class Card:
	def __init__(self, suit: str, value: int):
		self.suit = suit
		self.value = value

	def get_suit(self):
		return self.suit

	def get_value(self):
		return self.value

	def set_suit(self, newSuit):
		self.suit = newSuit

	def set_value(self, newValue):
		self.value = newValue

	def __repr__(self):
		return f"{self.value} of {self.suit}"