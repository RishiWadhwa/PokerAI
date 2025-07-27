import random
from Agent.Qtable import QTable

class EpsilonGreedyPolicy:
	def __init__(self, epsilon, actions):
		self.epsilon = epsilon
		self.actions = actions

	def select_action(self, q_table, state):
		if random.random() < self.epsilon:
			return random.choice(self.actions)
		else:
			q_values = [q_table.get(state, a) for a in self.actions]
			max_q = max(q_values)

			best_actions = [a for a, q in zip(self.actions, q_values) if q == max_q]
			return random.choice(best_actions)