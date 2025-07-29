# PokerAI

## Table of Contents
1. [Folder Tree](#folder-tree)
2. [Key Files](#key-files)
	- [Key Files: DQN](#key-files-dqn)
	- [Key Files: Q-Learning](key-files-q)
3. [Training/Testing DQN Model](#train-dqn)
4. [Types of Executions](#executions)
5. [Statistic Calculations](#statistics)
6. [Limitations](#limitations)

---

## Poker AI Tree <a name='folder-tree'></a>
```
📦PokerAI
 ┣ 📂src
 ┃ ┣ 📂Agent
 ┃ ┃ ┣ 📜Agent.py
 ┃ ┃ ┣ 📜Parameters.py
 ┃ ┃ ┣ 📜Policy.py
 ┃ ┃ ┣ 📜Qtable.py
 ┃ ┃ ┗ 📜__init
 __.py
 ┃ ┣ 📂DQNAgent
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜dqn_agent.py
 ┃ ┃ ┣ 📜parameters.py
 ┃ ┃ ┣ 📜q_network.py
 ┃ ┃ ┣ 📜replay_buffer.py
 ┃ ┃ ┗ 📜state_encoder.py
 ┃ ┣ 📂Environment
 ┃ ┃ ┣ 📜BettingParameters.py
 ┃ ┃ ┣ 📜PokerActions.py
 ┃ ┃ ┣ 📜PokerEnv.py
 ┃ ┃ ┣ 📜RuleBasedPlayer.py
 ┃ ┃ ┣ 📜StateEncoder.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂GameEngine
 ┃ ┃ ┣ 📜.DS_Store
 ┃ ┃ ┣ 📜ActionSpace.py
 ┃ ┃ ┣ 📜Card.py
 ┃ ┃ ┣ 📜Deck.py
 ┃ ┃ ┣ 📜GameState.py
 ┃ ┃ ┣ 📜HandEvaluator.py
 ┃ ┃ ┣ 📜Player.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂Training
 ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┣ 📜test_dqn.py
 ┃ ┃ ┣ 📜test_ql_agent.py
 ┃ ┃ ┣ 📜train_dqn.py
 ┃ ┃ ┗ 📜train_qlearning.py
 ┃ ┣ 📂TrainingData
 ┃ ┃ ┣ 📂DQNAgent
 ┃ ┃ ┃ ┣ 📂betting-models
 ┃ ┃ ┃ ┃ ┗ 📜...
 ┃ ┃ ┃ ┣ 📂high-buffer-betting-models
 ┃ ┃ ┃ ┃ ┗ 📜...
 ┃ ┃ ┃ ┣ 📂models
 ┃ ┃ ┃ ┃ ┗ 📜...
 ┃ ┃ ┗ 📜qtable.pkl
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜GameLoop.py
 ┃ ┣ 📜dqn_v_player_test.py
 ┃ ┗ 📜run_dqn_playbook.py
 ┣ 📜LICENSE
 ┗ 📜README.md
```

---

## Key Files: <a name='key-files'></a>

### DQN Model (Deep Q-Learning Network/Deep Q-Network) <a name='key-files-dqn'></a>
- Supports betting features
- **dqn_agent:** DQN Agent
- **parameters:** DQN-specific parameters (training/testing)
- **q_network:** DQN tensors and matrix calculations
- **replay_buffer:** Stores past experiences from learned samples in the form of tuples that are serialized.
- **state_encoder:** Normalizes the state for AI recollection in models to determine most likely to-do

Current win rate *~70%* with payout at *200 chips / 1,000 chips*.

Data of the DQN model with betting is stored in `TrainingData/DQNAgent/betting-models`. Obsolete DQN model without betting is stored in `TrainingData/DQNAgent/models`. 
- The non-betting model was trained on a randomized player as found in `Environment/RuleBasedPlayer.py` with the `choose_action()` function
- The betting model was trained on a rule-based player that roughly demonstrates basic poker knowledge and capacity. The rule-based player can be found in `Environment/RuleBasedPlayer.py` in the `choose_rule_based_action()` function which introduces a degree of uncertainty that most players would have when raising demonstrated with the function of that same file: `determine_raise_amt()`.
	- It should be noted that because the AI was trained against a reasonable uncertainty-based raising model, it also exhibits a similar degree of uncertainty when raising. Meaning, when running the exact same circumstance multiple times, it is possible the AI switches it's raise amount. *However, this change will not be drastic (i.e. 10 --> 200), instead it will be slight (i.e. 10 --> 50).*

###### **NOTE: non-betting models cannot be retrained nor used in existing codebase**

###### **NOTE 2: *\_\_ chip / \_\_ chips* payout refers to the approximate payout gained. For instance while it may say that `DQN_BETTING_MODEL_PATH` offers a *200 chip / 1,000 chips* this refers to average per game win. After running 8 games winning 2 hands I was up 600 chips. Winnings depend on circumstance.**

### Q-Learning Model (No bets + Outdated/Cannot be retrained or demonstrated in current codebase) <a name='key-files-q'></a>
- **Agent:** Q-Learning Agent
- **Parameters:** Parameters for the Q-Learning Agent
- **Policy:** Q-Learning Policy Net (Target Net derived from it)
- **Qtable:** Standard Q-Learning table for poker

Data of training the Q-learning model is in `TrainingData/qtable.pkl`

---

## Training/Testing DQN Model: <a name='train-dqn'></a>

To train or test the DQN enter the `PokerAI/src/` folder and run either of the following commands:
- `python3 -m Training.train_dqn` - Trains the dqn model according to specifications set in: `DQNAgent/parameters.py`
- `python3 -m Training.test_dqn` - Tests the dqn model according to specifications set in `DQNAgent/parameters.py`

###### **NOTE: `python3` can and should be substituted with `python` instead if the system dictates it. My system requires use of running `python3` so logs are formatted as such.**

Relevant Parameters for Training:
1. `BUFFER_SIZE`: How much information can be stored by the AI before resetting the buffer and clearing old learned experiences
2. `BATCH_SIZE`: How many experiences are sampled per training step.
3. `LR`: (Learning Rate) | How aggressively the model updates weight
4. `GAMMA`: (Discount Factor) | Controls how much future rewards are considered.
5. `EPSILON_START`: Initial exploration value. 0-->1 where 1 represents all exploration and 0 represents all learned information
6. `EPSILON_MIN`: Sets the minimum for training sets at what point should the AI stop exploring and start recalling
7. `EPSILON_DECAY`: Sets the decay rate of how much the AI should favor learned experiences vs exploring
8. `TARGET_UPDATE_FREQ`: How often to sync target network, in unit of steps
9. `NUM_EPISODES`: How many training episodes should be ran.
10. `MAX_STEPS_PER_EPISODE`: How far into the simulated future should the model view.
11. `SAVE_MODEL_EVERY`: How often should the model save itself.

Relevant Parameters for Testing:
1. `NUM_TEST_EPISODES`: Number of tests the model should run.
2. `DISPLAY_EVERY`: How often to print logs of the test during its evaluation as the `NUM_TEST_EPISODES` may be more than a reasonable number of logs for the user to read. Essentially highlights an evaluation after every some dictated amount.

Model Saves:
1. `DQN_MODEL_PATH`: Path to the model for non-betting in both training/testing
2. `DQN_BETTING_MODEL_PATH`: Path to the model for betting in both training/testing

---

## Types of Executions: <a name='executions'></a>

Currently this is/these are the supported execution(s). Execution(s) should be run from `PokerAI/src/` folder, and will not compile if ran elsewhere.
1. `rule_dqn_playbook.py` : `python3 -m run_dqn_playbook` - Will execute a script allowing you to input your hand and the board repeatedly to recieve an instruction of what the AI suggests you do.
	- Known bug: the AI sometimes executes `FOLD` instead of `CHECK`. This is because the `CHECK` system was not implemented. When `CHECK` is an available play, make sure you call `CHECK`. 
	- This was fixed, but *in case* an instance doesn't get caught, use `CHECK` instead of `FOLD`.
	- You can run the program with a high buffer algorithm instead of the usual buffer algorithm. For this switch `DQN_BETTING_MODEL_PATH` to `DQN_BETTING_HIGH_BUFFER_MODEL_PATH`.
		- `DQN_BETTING_HIGH_BUFFER_MODEL_PATH` offers a *~70%* with *100 chip / 1,000 chips* payout, but is more refined and precise in comparison with the `DQN_BETTING_MODEL_PATH`

###### **NOTE: `python3` can and should be substituted with `python` instead if the system dictates it. My system requires use of running `python3` so logs are formatted as such.**

###### **NOTE 2: *\_\_ chip / \_\_ chips* payout refers to the approximate payout gained. For instance while it may say that `DQN_BETTING_MODEL_PATH` offers a *200 chip / 1,000 chips* this refers to average per game win. After running 8 games winning 2 hands I was up 600 chips. Winnings depend on circumstance.**

---

## Statistic Calculations <a name='statistics'></a>

According to research this is the average benchmarks of a poker AI:

| AI Strength | Win Rate bb/100 |
| ------------|-----------------|
| Random AI   | ~0 or < 0       |
| Rule-Based AI | -10 to +5     |
| Q-Learning/Basic DQN | 0 to +19 |
| Strong DQN | +20 to +50       |
| Near Optimal AI (Libratus-, DeepStack-level) | +50 and higher |

The win rate (bb / 100) can be calculated by using the equation: `bb/100 = [ (Net chips [win/lost] + Initial Chips) / Big Blind Amount ] * (100 / Total Hands Played)`.

My AI was under specific instructions to ignore blinds but also doesn't fold on first round, making it to `FLOP` unless given a disastrously 2 of Hearts and 9 of Spades type hand. For that reason to calculate my specific `bb/100` or *ROI* I used this equation: `CHIP ROI % = (100 * Net Chips) / (Games Played * Initial Chips per Game)`.

Calculating this at my specifications of ~70% win rate with a 200 chip payout per 1,000 initial: `CHIP ROI % = (100 * 200,000) / (1,000 * 1,000) = 20,000,000 / 1,000,000 = 20%`.

The finally calculations indicate this model has a *20%* ROI Equating to the estimated goal of making a strong DQN model.

---

## Limitations <a name='limitations'></a>

The biggest limitation I noticed in this was the CPU power needed to train the AI. With my resources I couldn't exceed 100,000 training episodes with a maximum step size of 1,000 steps. When I pushed to 1,000,000 training episodes the terminal window consistently froze or stopped responding, requiring me to force quit it. With a higher CPU power and more RAM I may have ben able to push farther and better refine my AI.

Additionally, the AI tensors are optimized to run on the CUDA-enabled NVIDIA GPU system, which would have significantly improved runtime and training efficiency. However, since I ran the simulation and training/testing on a Mac — which lacks native CUDA support — I was limited to CPU-based tensor operations. As a result, my training and testing times were considerably longer.
