from GameEngine.GameState import GameState
from GameEngine.Card import Card
from DQNAgent.dqn_agent import DQNAgent
from Environment.PokerActions import PokerActions, PlayerAction
import Environment.BettingParameters as betting_params
from DQNAgent.state_encoder import encode_state_dqn
import DQNAgent.parameters as dqn_params

import os
import torch

def str_to_card(card_str):
    """Converts string like 'AH' or '10D' to Card object with int value."""
    rank_str_to_value = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    card_str = card_str.strip().upper()

    if len(card_str) < 2:
        raise ValueError("Invalid card input")

    if card_str.startswith("10"):
        rank = "10"
        suit = card_str[2:]
    else:
        rank = card_str[0]
        suit = card_str[1:]

    if rank not in rank_str_to_value:
        raise ValueError(f"Invalid rank: {rank}")
    if suit not in ["H", "D", "S", "C"]:
        raise ValueError(f"Invalid suit: {suit}")

    return Card(suit=suit, value=rank_str_to_value[rank])


def get_hand_input(prompt):
    while True:
        try:
            hand_str = input(prompt).strip().split()
            return [str_to_card(card_str) for card_str in hand_str]
        except Exception as e:
            print(f"Invalid format. Example: AH KD 9S (Ace of Hearts, King of Diamonds, 9 of Spades)\n[Error] {e}")

def main():
    print("=== Poker DQN Advisor ===")
    
    game_state = GameState(players=["AI1"], debug=False)

    hand = get_hand_input("Enter your hand (e.g., AH KD): ")
    game_state.set_ai_hand(hand)


    board = get_hand_input("Enter current board (e.g., 10H JS QC) or leave blank: ")
    game_state.set_board(board)


    if len(board) == 0:
        game_state.game_phase = game_state.get_phase().PRE_FLOP
    elif len(board) == 3:
        game_state.game_phase = game_state.get_phase().FLOP
    elif len(board) == 4:
        game_state.game_phase = game_state.get_phase().TURN
    elif len(board) == 5:
        game_state.game_phase = game_state.get_phase().RIVER


    state = encode_state_dqn(game_state, None, "AI1")

    can_check = input("Can you check? (yes/no) ")
    can_check_bool = False
    while can_check.lower() != "yes" and can_check.lower() != "no":
        can_check = input("Invalid. Can you check? (yes/no) ")

    if can_check.lower() == "yes":
        can_check_bool = True


    agent = DQNAgent(
        state_size=len(state),
        action_size=len(PokerActions) - 1 + len(betting_params.RAISE_SIZES),
        device=torch.device("cpu")
    )
    
    model_file = os.path.join(dqn_params.DQN_BETTING_MODEL_PATH, f"dqn_ep{dqn_params.NUM_EPISODES}.pth")
    agent.load(model_file)

    action = agent.choose_action(state)
    
    if action.action_type == PokerActions.FOLD and can_check_bool:
        print(f"\n💡 Recommended Action: CHECK", end="")
    else:
        print(f"\n💡 Recommended Action: FOLD", end="")

    if action.action_type == PokerActions.RAISE:
        print(f" ${action.amount}")
    else:
        print()

    inputted = input("Press 'q' to leave. ")
    if inputted.lower() != "q":
        main()

if __name__ == "__main__":
    main()
