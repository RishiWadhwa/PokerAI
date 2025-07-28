import os
import random
import numpy as np
import torch

from DQNAgent.dqn_agent import DQNAgent
from DQNAgent.state_encoder import encode_state_dqn
import DQNAgent.parameters as dqn_params

import Environment.BettingParameters as betting_params
from Environment.PokerEnv import PokerEnv
from Environment.PokerActions import PokerActions

def train():
    players = ["AI1", "P1"]
    env = PokerEnv(players)
    player_names = players  # just the list

    state = env.reset()  # encoded vector from env

    state_size = len(state)
    action_size = len(PokerActions) + len(betting_params.RAISE_SIZES) - 1

    agent = DQNAgent(state_size, action_size, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    for episode in range(1, dqn_params.NUM_EPISODES + 1):
        state = env.reset(use_dqn=True)
        done = False
        total_reward = 0
        last_opponent_action = None

        for step in range(dqn_params.MAX_STEPS_PER_EPISODE):
            # state is already encoded state vector
            action = agent.choose_action(state)

            next_state, reward, done, info = env.step(action, use_dqn=True)

            agent.step(state, action, reward, next_state, done)

            total_reward += reward
            state = next_state  # already encoded

            if done:
                break        

        if episode % dqn_params.SAVE_MODEL_EVERY == 0:
            os.makedirs(dqn_params.DQN_MODEL_PATH, exist_ok=True)
            save_path = os.path.join(dqn_params.DQN_MODEL_PATH, f"dqn_ep{episode}.pth")
            agent.save(save_path)

            print(f"Episode {episode} - Total Reward: {total_reward:.2f} - Epsilon: {agent.epsilon:.4f}")
            print(f"Saved model to {save_path}")


if __name__ == "__main__":
	train()

