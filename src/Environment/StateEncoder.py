from GameEngine.HandEvaluator import HandEvaluator
from Environment.PokerActions import PokerActions
from GameEngine.GameState import GameState

def encode_state(game_state: GameState, last_opponent_action: PokerActions, current_player: str):
	"""
	Returns list/numpy array of current state

	Args:
	- game_state: GameState obj
	- last_opponent_action: PokerActions enum with default/acceptable value of None
	- current_player: name of the current player
	"""

	player = game_state.players[current_player]
	evaluator = HandEvaluator(player.get_cards(), game_state.board)
	hand_eval = evaluator.evaluate_hand()

	hand_strength = hand_eval[0]
	kickers = hand_eval[1:]

	MAX_KICKERS = 3
	kickers += [0] * (MAX_KICKERS - len(kickers))
	kickers = kickers[:MAX_KICKERS]

	# pot tracking
	pot_size = getattr(game_state, 'pot', 0)
	max_pot = 100 # example max pot
	norm_pot = pot_size / max_pot # 0 until implemented

	# Last opponent action encoding
	action_encoding = 0
	if last_opponent_action == PokerActions.FOLD:
		action_encoding = 1
	elif last_opponent_action == PokerActions.CALL:
		action_encoding = 2
	elif last_opponent_action == PokerActions.RAISE:
		action_encoding = 3

	phase_encoding = game_state.get_phase().value

	# Normalization = current / max outcomes
	state_vector = [
		hand_strength / 10, # normalized hand strength,
		*(k / 14 for k in kickers), # normalized card value
		norm_pot,
		action_encoding / 3,
		phase_encoding / 5
	]

	return state_vector

	