from Environment.PokerActions import PokerActions, PlayerAction
from GameEngine.GameState import GameState, PokerStages
from GameEngine.Card import Card
from GameEngine.HandEvaluator import HandEvaluator
import Environment.BettingParameters as betting_params

import random

class RuleBasedPlayer:
	def choose_action(self, state):
		return random.choice([PokerActions.FOLD, PokerActions.CALL, PokerActions.RAISE])

	def choose_rule_based_action(self, state, player_hand, max_chips):
		hand_evaluator = HandEvaluator(player_hand, state.board)
		evaluation = hand_evaluator.evaluate_hand()

		hand_ranking = evaluation[0]
		kickers = evaluation[1:]

		if state.get_phase() == PokerStages.PRE_DEAL or state.get_phase() == PokerStages.PRE_FLOP:
			if hand_ranking <= 2:
				return PlayerAction(PokerActions.CALL)
			return PlayerAction(PokerActions.RAISE, self.determine_raise_amt(hand_ranking, max_chips))
		elif state.get_phase() == PokerStages.FLOP:
			if hand_ranking == 1:
				return PlayerAction(PokerActions.FOLD)

			if hand_ranking >= 3:
				return PlayerAction(PokerActions.RAISE, self.determine_raise_amt(hand_ranking, max_chips))

			return PlayerAction(PokerActions.CALL)
		elif state.get_phase() == PokerStages.TURN:
			if hand_ranking <= 4:
				return PlayerAction(PokerActions.CALL)

			return PlayerAction(PokerActions.RAISE, self.determine_raise_amt(hand_ranking, max_chips))
		elif state.get_phase() == PokerStages.RIVER:
			if hand_ranking <= 4:
				return PlayerAction(PokerActions.CALL)

			return PlayerAction(PokerActions.RAISE, self.determine_raise_amt(hand_ranking, max_chips))

		return PlayerAction(PokerActions.CALL)

	def determine_raise_amt(self, rank:int, max_chips:int) -> int:
		if rank in (1, 2, 3, 4):
			return min(betting_params.RAISE_SIZES[0], max_chips)
		elif rank in (5, 6, 7):
			return min(random.choice(betting_params.RAISE_SIZES[:2]), max_chips)
		elif rank == 8:
			return min(random.choice(betting_params.RAISE_SIZES[1:3]), max_chips)
		elif rank == 9:
			return min(random.choice(betting_params.RAISE_SIZES[1:4]), max_chips)
		else:
			return min(random.choice(betting_params.RAISE_SIZES[2:]), max_chips)