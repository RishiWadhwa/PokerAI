from Card import Card
from typing import List

class Player:
	def __init__(self, is_active: bool):
		self.cards = List[Card]
		self.is_active = is_active

	def add_card(self, card: Card):
		self.cards.append(card)

	def get_cards(self) -> List[Card]:
		return self.cards

	def fold(self):
		self.is_active = False

	def get_status(self) -> bool:
		return self.is_active
