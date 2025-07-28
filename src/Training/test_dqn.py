import torch
import os

from DQNAgent.dqn_agent import DQNAgent
from DQNAgent.state_encoder import encode_state_dqn
import DQNAgent.parameters as dqn_params
from Environment.PokerActions import PokerActions
from Environment.PokerEnv import PokerEnv
import Environment.BettingParameters as betting_params

def test(num_episodes=dqn_params.NUM_TEST_EPISODES, model_path=None, players=["AI1", "P1"]):
	env = PokerEnv(players)
	player_names = env.players

	initial_state = env.reset(use_dqn=True)
	state_size = len(initial_state)
	action_size = len(PokerActions) + len(betting_params.RAISE_SIZES) - 1

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	agent = DQNAgent(state_size, action_size, device=device)

	# Load path
	if model_path and os.path.isfile(model_path):
		agent.load(model_path)
		print(f"Loaded model: {model_path}")
	else:
		print("Model path invalid or not provided. Exiting test.")
		return

	# Disable exploration, rely on learned information
	agent.epsilon = 0.0
	
	# Metric tracking for analysis
	total_rewards = 0
	wins = 0

	for episode in range(1, num_episodes + 1):
		state = env.reset(use_dqn=True)
		done = False
		episode_reward = 0

		while not done:
			action = agent.choose_action(state)
			next_state, reward, done, info = env.step(action, use_dqn=True)

			episode_reward += reward
			state = next_state

		total_rewards += episode_reward
		if info.get("winner") == "AI1":
			wins += 1

		if episode % dqn_params.DISPLAY_EVERY == 0:
			print(f"Episode {episode} completed. Reward={episode_reward}, Winner={info.get('winner')}")

	print(f"\nTest completed over {num_episodes}")
	print(f"Win Rate: {wins / num_episodes * 100:.2f}%")
	print(f"Average reward per episode: {total_rewards / num_episodes:.3f}")

if __name__ == "__main__":
	model_file = os.path.join(dqn_params.DQN_MODEL_PATH, f"dqn_ep{dqn_params.NUM_EPISODES}.pth")
	test(model_path=model_file)