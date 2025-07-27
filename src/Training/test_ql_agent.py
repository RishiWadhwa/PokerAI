import Agent.Parameters as params
from Agent.Agent import QLearningAgent
from Environment.PokerActions import PokerActions
from Environment.PokerEnv import PokerEnv

def test():
	players = ["AI1", "P1"]
	env = PokerEnv(players)
	agent = QLearningAgent()
	agent.load(params.Q_LEARNING_FILE)

	num_tests = 100
	wins = 0
	total_reward = 0

	for _ in range(num_tests):
		state = env.reset()
		done = False
		epsilon_reward = 0

		while not done:
			action = agent.choose_action(state)
			next_state, reward, done, info = env.step(action, debug=True)

			epsilon_reward += reward
			state = next_state

		total_reward += epsilon_reward

		winner = info.get("winner")
		if winner == "AI1":
			wins += 1

	win_rate = wins/num_tests
	avg_reward = total_reward/num_tests
	print(f"Tested: {num_tests}. Won: {win_rate:.2%}. Average Reward: {avg_reward:.2f}")

if __name__ == "__main__":
	test()