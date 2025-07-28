import torch
import os

from DQNAgent.dqn_agent import DQNAgent
from DQNAgent.state_encoder import encode_state_dqn
import DQNAgent.parameters as dqn_params

import Environment.BettingParameters as betting_params
from Environment.PokerEnv import PokerEnv
from Environment.PokerActions import PokerActions

def human_vs_ai(model_path, players=["AI1", "human"], debug=False):
	env = PokerEnv(players)
	player_names = players

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	state = env.reset(use_dqn=True)

	state_size = len(state)
	action_size = len(PokerActions) + len(betting_params.RAISE_SIZES) - 1
	
	agent = DQNAgent(state_size, action_size, device=device)
	agent.load(model_path)
	agent.epsilon = 0.0

	done = False
	last_opponent_action = None

	print("Starting Poker: Human v AI\nAvailable Actions: Fold, Call, Raise")

	while not done:
		current_player = env.players[env.current_player_index]

		if current_player == "AI1":
			state_enc = encode_state_dqn(env.game_state, last_opponent_action, current_player)
			action = agent.choose_action(state_enc)
			print(f"AI chooses: {action.name.lower()}")
		else:
			# Human turn, take input
			valid_input = False
			while not valid_input:
				human_action = input("Your move (fold/call/raise): ").strip().lower()
				if human_action in ["fold", "call", "raise"]:
					action = PokerActions[human_action.upper()]
					valid_input = True
				else:
					print("Invalid input. Try again.")
			print("\n\n\n")

		next_state, reward, done, info = env.step(action, human_action=action, use_dqn=True)

		last_opponent_action = action

		env.render()		
		
		if debug:
			print(f"Reward This Turn: {reward}")

	winner = info.get("winner")
	if winner == "human":
		print("Congrats! You Won!")
	elif winner == "AI1":
		print("AI wins this time!")
	else:
		print("Game ended with no clear winner.")

if __name__ == "__main__":
	model_file = os.path.join(dqn_params.DQN_MODEL_PATH, f"dqn_ep{dqn_params.NUM_EPISODES}.pth")
	human_vs_ai(model_file)
