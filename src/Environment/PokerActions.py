from enum import Enum

class PokerActions(Enum):
	FOLD = 0
	CALL = 1
	RAISE = 2

class PlayerAction:
	def __init__(self, action_type: PokerActions, amount:int=0):
		self.action_type = action_type
		self.amount = amount

	def __repr__(self):
		return f"{self.action_type.name}({self.amount})" if self.action_type == PokerActions.RAISE else self.action_type.name