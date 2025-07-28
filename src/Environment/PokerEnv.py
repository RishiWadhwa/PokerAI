from GameEngine.GameState import GameState, PokerStages
from Environment.StateEncoder import encode_state
from Environment.PokerActions import PokerActions, PlayerAction
from Environment.RuleBasedPlayer import RuleBasedPlayer
from DQNAgent.state_encoder import encode_state_dqn

import Environment.BettingParameters as betting_params

class PokerEnv:
	def __init__(self, players):
		self.players = players
		self.game_state = GameState(players)
		self.done = False
		self.current_player_index = 0
		self.last_opponent_action: PokerActions = None
		self.phase_start_player_index = 0
		self.rule_based_player = RuleBasedPlayer()

		self.pot = 0
		self.current_bet = 0
		self.current_bet_contributions = {player: 0 for player in self.players}

	def reset(self, use_dqn=False):
		self.game_state = GameState(self.players)
		self.done = False
		self.current_player_index = 0
		self.last_opponent_action = None
		self.phase_start_player_index = self.current_player_index
		state = self._get_state(use_dqn)

		self.pot = 0
		self.current_bet = 0

		self.current_bet_contributions = {player: 0 for player in self.players}

		for p in self.players:
			self.game_state.players[p].reset()

		return state

	def step(self, ai_action:PlayerAction, human_action:PlayerAction=None, debug=False, use_dqn=False):
		"""
		- accept action
		- apply to gamestate
		- advance game logic
		"""
		current_player_name = self.players[self.current_player_index]
		current_player = self.game_state.players[current_player_name]

		# determine action
		if current_player_name == "AI1":
			action = ai_action
		elif human_action is not None:
			action = human_action
		else:
			action = self.rule_based_player.choose_rule_based_action(self.game_state, self.game_state.players[current_player_name].get_cards(), self.game_state.players[current_player_name].get_chips())

		action_type = action.action_type
		amount = action.amount


		# apply action to player
		if (action_type == PokerActions.FOLD):
			current_player.fold()
			self.last_opponent_action = PokerActions.FOLD
		elif (action_type == PokerActions.CALL):
			to_call = self.current_bet - self.current_bet_contributions[current_player_name]
			to_call = max(0, to_call)

			chips_paid = min(current_player.get_chips(), to_call)
			current_player.bet(chips_paid)
			self.pot += chips_paid

			self.current_bet_contributions[current_player_name] += chips_paid
			self.last_opponent_action = PokerActions.CALL
		elif (action_type == PokerActions.RAISE):
			self.last_opponent_action = PokerActions.RAISE

			raise_amount = amount if amount is not None else betting_params.RAISE_SIZES[0]

			new_bet = self.current_bet + raise_amount
			to_put_in = new_bet - self.current_bet_contributions[current_player_name]

			chips_paid = min(current_player.get_chips(), to_put_in)
			current_player.bet(chips_paid)
			self.pot += chips_paid

			self.current_bet = max(self.current_bet, self.current_bet_contributions[current_player_name] + chips_paid)
			self.current_bet_contributions[current_player_name] += chips_paid

		self.current_player_index = (self.current_player_index + 1) % len(self.players)

		if self.current_player_index == self.phase_start_player_index:
			self.game_state.advance_phase()
			self.phase_start_player_index = self.current_player_index
			self.current_bet = 0 # reset bet in new phase

			self.current_bet_contributions = {player: 0 for player in self.players}

		active_players = [p for p in self.players if self.game_state.players[p].get_status()]
		if len(active_players) == 1:
			winner = active_players[0]
			self.done = True
			self.game_state.winner = winner
			self.game_state.players[winner].win_chips(self.pot)

			reward = 1 if winner == "AI1" else -1
		elif self.game_state.get_phase() == PokerStages.REVEAL:
			self.done = True
			winner = self.game_state.determine_winner()
			self.game_state.winner = winner
			self.game_state.players[winner].win_chips(self.pot)

			reward = 1 if winner == "AI1" else -1
		else:
			reward = 0
			winner = None

		state = self._get_state(use_dqn)
		info = {'winner': winner}
		if debug:
			print(f"Action: {action_type.name}, Agent: {current_player_name}, Reward: {reward}, Pot: {self.pot}, Bet to Call: {self.current_bet}")
		return state, reward, self.done, info

	def _get_state(self, use_dqn):
		current_player = self.players[self.current_player_index]
		if use_dqn:
			return encode_state_dqn(self.game_state, self.last_opponent_action, current_player)
		else:
			return encode_state(self.game_state, self.last_opponent_action, current_player)

	def render(self):
		print(f"Phase: {self.game_state.get_phase().name}")
		print(f"Board: {self.game_state.board}")

		for player_name in self.players:
			hand = self.game_state.players[player_name].get_cards()
			status = 'Active' if self.game_state.players[player_name].get_status() else 'Folded'

			print(f"{player_name} - {status}: {hand}")