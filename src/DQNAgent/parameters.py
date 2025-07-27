
# replay buffer size
BUFFER_SIZE = 1_000

# mini-batch size for training
BATCH_SIZE = 64

# learning rate
LR = 1e-3

# discount factor
GAMMA = 0.99

# epsilon parameters
EPSILON_START = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

# update frequency of the target network (unit: number of steps)
TARGET_UPDATE_FREQ = 1_000