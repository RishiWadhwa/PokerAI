import random
from typing import List
from Card import Card

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