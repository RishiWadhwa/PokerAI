import Agent.Parameters as params
from Agent.Agent import QLearningAgent
from Environment.PokerEnv import PokerEnv
from Environment.PokerActions import PokerActions

def train():
	players = ["AI1", "P1"]
	env = PokerEnv(players)
	agent = QLearningAgent()

	for episode in range(params.NUM_EPISODES):
		state = env.reset()
		done = False

		while not done:
			action = agent.choose_action(state)
			next_state, reward, done, info = env.step(action, debug=True)

			agent.learn(state, action, reward, next_state, done)
			state = next_state

		agent.decay_epsilon()

		if (episode + 1) % 100 == 0:
			print(f"Episode {episode + 1} completed, Epsilon: {agent.epsilon:.4f}")

	# save data
	agent.save(params.Q_LEARNING_FILE)

if __name__ == "__main__":
	train()