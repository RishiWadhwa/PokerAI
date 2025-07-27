import random
from collections import deque
import numpy as np

class ReplayBuffer:
	def __init__(self, buffer_size, batch_size):
		self.memory = deque(maxlen=buffer_size)
		self.batch_size = batch_size

	def add(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))

	def sample(self, batch_size=None):
		batch_size = batch_size or self.batch_size
		batch = random.sample(self.memory, batch_size)

		states, actions, rewards, next_states, dones = zip(*batch)

		return (
			np.array(states),
			np.array(actions),
			np.array(rewards, dtype=np.float32),
			np.array(next_states),
			np.array(dones, dtype=np.uint8)
		)

	def __len__(self):
		return len(self.memory)