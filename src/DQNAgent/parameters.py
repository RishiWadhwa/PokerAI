
# replay buffer size
BUFFER_SIZE = 100_000

# mini-batch size for training
BATCH_SIZE = 64

# learning rate
LR = 1e-3

# discount factor
GAMMA = 0.99

# epsilon parameters
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.99999

# update frequency of the target network (unit: number of steps)
TARGET_UPDATE_FREQ = 1_000

# Path saving
DQN_MODEL_PATH = "TrainingData/DQNAgent/models/"
DQN_BETTING_MODEL_PATH = "TrainingData/DQNAgent/betting-models/"

# Training metrics
NUM_EPISODES = 100_000
MAX_STEPS_PER_EPISODE = 1_000
SAVE_MODEL_EVERY = 10_000

# Testing metrics
NUM_TEST_EPISODES = 10_000
DISPLAY_EVERY = 1_000