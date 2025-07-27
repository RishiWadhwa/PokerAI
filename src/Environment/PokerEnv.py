from GameEngine.GameState import GameState, PokerStages
from Environment.StateEncoder import encode_state
from Environment.PokerActions import PokerActions
from Environment.RuleBasedPlayer import RuleBasedPlayer

class PokerEnv:
	def __init__(self, players):
		self.players = players
		self.game_state = GameState(players)
		self.done = False
		self.current_player_index = 0
		self.last_opponent_action: PokerActions = None
		self.phase_start_player_index = 0
		self.rule_based_player = RuleBasedPlayer()

	def reset(self):
		self.game_state = GameState(self.players)
		self.done = False
		self.current_player_index = 0
		self.last_opponent_action = None
		self.phase_start_player_index = self.current_player_index
		state = self._get_state()

		return state

	def step(self, ai_action: PokerActions, debug=False):
		"""
		- accept action
		- apply to gamestate
		- advance game logic
		"""
		current_player = self.players[self.current_player_index]

		# determine action
		if current_player == "AI1":
			action = ai_action
		else:
			action = self.rule_based_player.choose_action(self._get_state())

		# apply action to player
		if (action == PokerActions.FOLD):
			self.game_state.players[current_player].fold()
			self.last_opponent_action = PokerActions.FOLD
		elif (action == PokerActions.CALL):
			self.last_opponent_action = PokerActions.CALL
			# implement call w betting later
		elif (action == PokerActions.RAISE):
			self.last_opponent_action = PokerActions.RAISE
			# implement later w beeting

		self.current_player_index = (self.current_player_index + 1) % len(self.players)

		if self.current_player_index == self.phase_start_player_index:
			self.game_state.advance_phase()
			self.phase_start_player_index = self.current_player_index

		active_players = [p for p in self.players if self.game_state.players[p].get_status()]
		if len(active_players) == 1:
			winner = active_players[0]
			self.done = True

			reward = 1 if winner == "AI1" else -1
		else:
			reward = 0
			winner = None

		state = self._get_state()
		info = {'winner': winner}
		if debug:
			print(f"Action: {action}, Agent: {current_player}, Reward: {reward}")
		return state, reward, self.done, info

	def _get_state(self):
		current_player = self.players[self.current_player_index]
		return encode_state(self.game_state, self.last_opponent_action, current_player)

	def render(self):
		print(f"Phase: {self.game_state.get_phase().name}")
		print(f"Board: {self.game_state.board}")

		for player_name in self.players:
			hand = self.game_state.players[player_name].get_cards()
			status = 'Active' if self.game_state.players[player_name].get_status() else 'Folded'

			print(f"{player_name} - {status}: {hand}")