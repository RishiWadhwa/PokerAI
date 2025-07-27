from Agent.Qtable import QTable
import Agent.Parameters as params
from Agent.Policy import EpsilonGreedyPolicy
from Environment.PokerActions import PokerActions


class QLearningAgent:
	def __init__(self):
		self.table = QTable()

		self.epsilon = params.EPSILON_START
		self.alpha = params.ALPHA
		self.gamma = params.GAMMA

		self.actions = list(PokerActions)

		self.policy = EpsilonGreedyPolicy(self.epsilon, self.actions)

	def choose_action(self, state):
		return self.policy.select_action(self.table, state)

	def learn(self, state, action, reward, next_state, done):
		current_q = self.table.get(state, action)

		if done:
			target = reward
		else:
			next_q_values = [self.table.get(next_state, a) for a in self.actions]
			target = reward + self.gamma * max(next_q_values)

		new_q = current_q + self.alpha * (target - current_q) # Bellman equation (RL): V(s) = max[ R(s,a) + y * sig{ P(s,a,s') * V(s') } ]
		self.table.set(state, action, new_q)

	def decay_epsilon(self): # reduce need for error in future as AI learns via RL
		self.epsilon = max(params.EPSILON_MIN, self.epsilon * params.EPSILON_DECAY) # max( e-min, e * DR )
		self.policy.epsilon = self.epsilon

	def save(self, path):
		self.table.save(path)

	def load(self, path):
		self.table.load(path)