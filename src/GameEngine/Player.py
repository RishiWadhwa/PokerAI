from GameEngine.Card import Card
from typing import List
import Environment.BettingParameters as betting_params

class Player:
	def __init__(self, is_active: bool):
		self.cards: List[Card] = []
		self.is_active = is_active
		self.chips = betting_params.STARTING_CHIPS

	def add_card(self, card: Card):
		self.cards.append(card)

	def get_cards(self) -> List[Card]:
		return self.cards

	def fold(self):
		self.is_active = False

	def get_status(self) -> bool:
		return self.is_active

	def get_chips(self) -> int:
		return self.chips

	def bet(self, amount:int) -> int:
		self.chips -= amount
		return self.get_chips()

	def win_chips(self, amount:int) -> int:
		self.chips += amount
		return self.get_chips()

	def reset(self):
		self.cards = []
		self.is_active = True
		self.chips = betting_params.STARTING_CHIPS