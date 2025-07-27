import random
from typing import List

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

class Deck:
	def __init__(self):
		# deck initialization here as an array of cards
		self.deck: List[Card] = []
		self.burned_deck: List[Card] = []

		suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
		values = list(range(2,15)) # list with ace high values

		for suit in suits:
			for value in values:
				self.deck.append(Card(suit, value))

	def shuffle_deck(self):
		random.shuffle(self.deck)

	def draw_card(self) -> Card:
		if not self.deck:
			raise IndexError("Cannot draw from empty deck.")
		card = self.deck.pop()

		self.burned_deck.append(card)
		return card

	def is_deck_empty(self) -> bool:
		return not self.deck