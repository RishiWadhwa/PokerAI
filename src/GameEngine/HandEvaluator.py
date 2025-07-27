from Card import Card
from enum import Enum
from typing import List

class HandStrength(Enum):
	HIGH = 1
	PAIR = 2
	TWO_PAIR = 3
	THREE_OF_A_KIND = 4
	STRAIGHT = 5
	FLUSH = 6
	FULL_HOSUE = 7
	FOUR_OF_A_KIND = 8
	STRAIGHT_FLUSH = 9
	ROYAL_FLUSH = 10

class HandEvaluator:
	def __init__(self, hand: List[Card], board: List[Card]):
		self.hand = hand
		self.board = board

	def update_hand(self, newHand):
		self.hand = newHand

	def update_board(self, newBoard):
		self.board = newBoard

	def get_hand(self) -> List[Card]:
		return self.hand

	def get_board(self) -> List[Card]:
		return self.board

	def evaluate_hand(self) -> [int, int]:
		cards = self.hand + self.board
		if not cards:
			return [-1, -1]

		value_counts = {}
		suit_counts = {}
		unique_values = set()

		for card in cards:
			value_counts[card.value] = value_counts.get(card.value, 0) + 1
			suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
			unique_values.add(card.value)

		sorted_values = sorted(unique_values)
		highest_value = max(sorted_values)

		# Flush Checker
		flush_suit = None
		for suit, count in suit_counts.items():
			if count >= 5:
				flush_suit = suit
				break

		# Straight Checker
		def has_straight(values):
			values = sorted(set(values))
			for i in range(len(values) - 4):
				if values[i] + 4 == values[i + 4] and all(values[i] + j in values for j in range(5)):
					return values[i + 4]
			# Special case: A-2-3-4-5
			if {14, 2, 3, 4, 5}.issubset(values):
				return 5
			return None

		straight_high = has_straight(sorted_values)

		# Straight flush / royal flush
		straight_flush_high = None
		if flush_suit:
			flush_cards = [c.value for c in cards if c.suit == flush_suit]
			straight_flush_high = has_straight(flush_cards)
			if straight_flush_high == 14:
				return [HandStrength.ROYAL_FLUSH.value, 14]
			elif straight_flush_high:
				return [HandStrength.STRAIGHT_FLUSH.value, straight_flush_high]

		# Other hands
		counts = sorted(value_counts.values(), reverse=True)
		pairs = [v for v, c in value_counts.items() if c == 2]
		threes = [v for v, c in value_counts.items() if c == 3]
		fours = [v for v, c in value_counts.items() if c == 4]

		if fours:
			return [HandStrength.FOUR_OF_A_KIND.value, highest_value]
		if threes and pairs:
			max_number = max(threes)
			if (max(pairs) > max_number):
				max_number = max(pairs)
			return [HandStrength.FULL_HOUSE.value, max_number]
		if flush_suit:
			return [HandStrength.FLUSH.value, highest_value]
		if straight_high:
			return [HandStrength.STRAIGHT.value, straight_high]
		if threes:
			return [HandStrength.THREE_OF_A_KIND.value, highest_value]
		if len(pairs) >= 2:
			return [HandStrength.TWO_PAIR.value, highest_value]
		if pairs:
			return [HandStrength.PAIR.value, highest_value]

		return [HandStrength.HIGH.value, highest_value]


