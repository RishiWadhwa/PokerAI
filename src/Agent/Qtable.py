import pickle

class QTable:
	def __init__(self):
		self.q_table = {} # ( (state, action), q-value) key-value pairs

	def get(self, state, action) -> float:
		return self.q_table.get((state, action), 0.0) # returns 0.0 if no action found

	def set(self, state, action, q_value):
		self.q_table[(state, action)] = q_value

	def save(self, path):
		with open(path, 'wb') as f:
			pickle.dump(self.q_table, f)

	def load(self, path):
		with open(path, 'rb') as f:
			self.q_table = pickle.load(f)
