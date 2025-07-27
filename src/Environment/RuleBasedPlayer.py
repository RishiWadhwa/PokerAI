from Environment.PokerActions import PokerActions
import random

class RuleBasedPlayer:
	def choose_action(self, state):
		return random.choice([PokerActions.FOLD, PokerActions.CALL, PokerActions.RAISE])