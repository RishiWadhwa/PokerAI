import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

from DQNAgent.q_network import QNetwork
from DQNAgent.replay_buffer import ReplayBuffer
import DQNAgent.parameters as dqn_params
from DQNAgent.state_encoder import encode_state_dqn

from Environment.PokerActions import PokerActions


class DQNAgent:
	def __init__(self, state_size, action_size, buffer_size=dqn_params.BUFFER_SIZE, batch_size=dqn_params.BATCH_SIZE, device=torch.device("cpu")):
		self.state_size = state_size
		self.action_size = action_size
		self.device = device

		self.policy_net: QNetwork = QNetwork(state_size, action_size).to(device)
		self.target_net: QNetwork = QNetwork(state_size, action_size).to(device)
		self.memory = ReplayBuffer(buffer_size, batch_size)
		self.target_net.load_state_dict(self.policy_net.state_dict())
		self.target_net.eval()

		self.optimizer = optim.Adam(self.policy_net.parameters(), lr=dqn_params.LR)
		
		self.batch_size = dqn_params.BATCH_SIZE
		self.gamma = dqn_params.GAMMA
		self.epsilon = dqn_params.EPSILON_START
		self.epsilon_min = dqn_params.EPSILON_MIN
		self.epsilon_decay = dqn_params.EPSILON_DECAY
		self.update_every = dqn_params.TARGET_UPDATE_FREQ

		self.step_count = 0

	def choose_action(self, state):
		if random.random() < self.epsilon:
			return random.choice(list(PokerActions))
		else:
			state_tensor = torch.tensor(state, dtype=torch.float32, device=self.device).unsqueeze(0)
			with torch.no_grad():
				q_values = self.policy_net(state_tensor)

			action_idx = q_values.argmax().item()
			return list(PokerActions)[action_idx]

	def step(self, state, action, reward, next_state, done):
		action_idx = list(PokerActions).index(action)
		self.memory.add(state, action_idx, reward, next_state, done)
		self.step_count += 1

		if len(self.memory) >= self.batch_size:
			self.learn()

		if self.step_count % self.update_every == 0:
			self.target_net.load_state_dict(self.policy_net.state_dict())

		self.epsilon = self.epsilon_decay * self.epsilon if self.epsilon > self.epsilon_min else self.epsilon

	def learn(self):
		states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

		states = torch.FloatTensor(states).to(self.device)
		next_states = torch.FloatTensor(next_states).to(self.device)

		actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
		rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
		dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

		q_values = self.policy_net(states).gather(1, actions)
		next_q_values = self.target_net(next_states).max(1)[0].detach().unsqueeze(1)
		target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))

		loss = nn.MSELoss()(q_values, target_q_values)

		self.optimizer.zero_grad()
		loss.backward()
		self.optimizer.step()

	def save(self, path):
		torch.save(self.policy_net.state_dict(), path)

	def load(self, path):
		self.policy_net.load_state_dict(torch.load(path, map_location=self.device))
		self.target_net.load_state_dict(self.policy_net.state_dict())







