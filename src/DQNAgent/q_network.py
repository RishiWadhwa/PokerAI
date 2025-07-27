import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
	def __init__(self, state_size: int, action_size: int, hidden_sizes=(64,64)):
		super(QNetwork, self).__init__()

		self.fc1 = nn.Linear(state_size, hidden_sizes[0])
		self.fc2 = nn.Linear(hidden_sizes[0], hidden_sizes[1])
		self.out = nn.Linear(hidden_sizes[1], action_size)

	def forward(self, state: torch.Tensor) -> torch.Tensor:
		x = F.relu(self.fc1(state))
		x = F.relu(self.fc2(x))

		q_values = self.out(x)
		return q_values