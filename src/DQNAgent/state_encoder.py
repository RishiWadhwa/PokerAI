from typing import List
from Environment.PokerActions import PokerActions
from GameEngine.HandEvaluator import HandEvaluator
from GameEngine.GameState import GameState
import Environment.BettingParameters as betting_params

import numpy as np

def encode_state_dqn(game_state: GameState, last_opponent_action: PokerActions, current_player: str) -> List[float]:
	"""
	Encodes the game state into a normalized feature vector for DQN input
	"""
	player = game_state.players[current_player]
	evaluator = HandEvaluator(player.get_cards(), game_state.board)
	hand_eval = evaluator.evaluate_hand()

	hand_strength = hand_eval[0]
	kickers = hand_eval[1:]

	# Pad/Truncate kickers to fixed length
	MAX_KICKERS = 3
	kickers += [0] * (MAX_KICKERS - len(kickers))
	kickers = kickers[:MAX_KICKERS]

	# Pot size + chips normalization
	pot_size = getattr(game_state, 'pot', 0)
	chips = player.get_chips()

	norm_pot = pot_size / betting_params.STARTING_CHIPS
	norm_chips = min(chips / betting_params.STARTING_CHIPS, 1.0)

	# current bet normalization
	current_bet = getattr(game_state, 'current_bet', 0)
	norm_current_bet = current_bet / betting_params.STARTING_CHIPS

	# Normalize hand strength, kickers
	norm_hand_strength = hand_strength / 10
	norm_kickers = [k / 14 for k in kickers]

	# Normalize pot
	pot_size = getattr(game_state, 'pot', 0)
	max_pot = 1_000
	norm_pot = min(pot_size / max_pot, 1.0)

	# Encode last opp action
	action_encoding = 0
	if last_opponent_action == PokerActions.FOLD:
		action_encoding = 1
	elif last_opponent_action == PokerActions.CALL:
		action_encoding = 2
	elif last_opponent_action == PokerActions.RAISE:
		action_encoding = 3

	norm_action = action_encoding / 5

	# Encode phase
	phase = game_state.get_phase().value
	norm_phase = phase / 5 # 5 phases: pre deal, pre flop, flop, turn, river, reveal

	state_vector = [
		norm_hand_strength,
		*(k / 14 for k in kickers),
		norm_pot,
		norm_current_bet,
		norm_chips,
		norm_action,
		norm_phase,
	]

	return np.array(state_vector, dtype=np.float32)

