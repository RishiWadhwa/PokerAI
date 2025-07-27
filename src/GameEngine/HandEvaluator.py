from GameEngine.Card import Card
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

	def evaluate_hand(self) -> List[int]:
		cards = self.hand + self.board
		if not cards:
		    return [-1]

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

		# Straight Checker helper
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


		straight_flush_high = None
		if flush_suit:
		    flush_cards = [c.value for c in cards if c.suit == flush_suit]
		    straight_flush_high = has_straight(flush_cards)
		    if straight_flush_high == 14:
		        # Royal flush
		        return [HandStrength.ROYAL_FLUSH.value, 14]
		    elif straight_flush_high:
		        return [HandStrength.STRAIGHT_FLUSH.value, straight_flush_high]


		counts_to_values = {}
		for val, count in value_counts.items():
		    counts_to_values.setdefault(count, []).append(val)

		for count in counts_to_values:
		    counts_to_values[count].sort(reverse=True)

		fours = counts_to_values.get(4, [])
		threes = counts_to_values.get(3, [])
		pairs = counts_to_values.get(2, [])
		singles = counts_to_values.get(1, [])
		singles = sorted(singles, reverse=True)

		# Helper to get kickers excluding certain values
		def get_kickers(exclude_values, count):
		    kickers = [v for v in sorted_values if v not in exclude_values]
		    kickers = sorted(kickers, reverse=True)
		    return kickers[:count]

		# Four of a kind
		if fours:
		    four_val = fours[0]
		    kickers = get_kickers([four_val], 1)
		    return [HandStrength.FOUR_OF_A_KIND.value, four_val] + kickers

		# Full house: three + pair
		if threes and (pairs or len(threes) > 1):
		    three_val = threes[0]
		    if len(threes) > 1:
		        pair_val = threes[1]
		    else:
		        pair_val = pairs[0]
		    return [HandStrength.FULL_HOSUE.value, three_val, pair_val]

		# Flush
		if flush_suit:
		    flush_cards = [c.value for c in cards if c.suit == flush_suit]
		    flush_cards = sorted(flush_cards, reverse=True)
		    return [HandStrength.FLUSH.value] + flush_cards[:5]

		# Straight
		if straight_high:
		    return [HandStrength.STRAIGHT.value, straight_high]

		# Three of a kind
		if threes:
		    three_val = threes[0]
		    kickers = get_kickers([three_val], 2)
		    return [HandStrength.THREE_OF_A_KIND.value, three_val] + kickers

		# Two pair
		if len(pairs) >= 2:
		    top_pair = pairs[0]
		    second_pair = pairs[1]
		    kickers = get_kickers([top_pair, second_pair], 1)
		    return [HandStrength.TWO_PAIR.value, top_pair, second_pair] + kickers

		# One pair
		if pairs:
		    pair_val = pairs[0]
		    kickers = get_kickers([pair_val], 3)
		    return [HandStrength.PAIR.value, pair_val] + kickers

		# High card
		high_cards = sorted_values[-5:]
		high_cards = sorted(high_cards, reverse=True)
		return [HandStrength.HIGH.value] + high_cards


