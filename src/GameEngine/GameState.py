from GameEngine.Deck import Deck
from GameEngine.Card import Card
from GameEngine.HandEvaluator import HandEvaluator
from typing import List, Dict
from enum import Enum
from GameEngine.Player import Player

class PokerStages(Enum):
    PRE_DEAL = 0
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    REVEAL = 5

class GameState:
    def __init__(self, players: List[str], debug=False):
        self.deck = Deck()
        self.deck.shuffle_deck()

        self.players: Dict[str, Player] = {}
        for player in players:
            self.players[player] = Player(True)

        # empty board
        self.board: List[Card] = []

        # initialize game phase
        self.game_phase = PokerStages.PRE_DEAL

        # winner
        self.winner: str = None  # use player name

        # debug
        self.debug = debug

    def initialize_hands(self):
        for _ in range(2):
            for player_name, player_obj in self.players.items():
                if player_obj.get_status():
                    player_obj.add_card(self.deck.draw_card())

        self.game_phase = PokerStages.PRE_FLOP

    def set_ai_hand(self, hand: List[Card]):
        self.players["AI1"].set_cards(hand)

    def set_board(self, board: List[Card]):
        self.board = board;

    def draw_to_board(self, count: int):
        for _ in range(count):
            self.board.append(self.deck.draw_card())

    def determine_winner(self) -> str:
        best_hand = None
        best_strength = [-1]  # initialize with a list for proper comparison
        winner = None

        for player_name, player_obj in self.players.items():
            if not player_obj.get_status():
                continue

            evaluator = HandEvaluator(player_obj.get_cards(), self.board)
            strength = evaluator.evaluate_hand()

            # Compare full strength lists lex order
            if strength > best_strength:
                best_strength = strength
                best_hand = evaluator
                winner = player_name

        return winner

    def get_phase(self) -> PokerStages:
        return self.game_phase

    def display_phase(self):
        print(f"=== Phase: {self.game_phase.name} ===")
        print("Board:", [str(card) for card in self.board])

        for player_name, player_obj in self.players.items():
            if player_obj.get_status():
                print(f"{player_name}'s Hand: {[str(card) for card in player_obj.get_cards()]}")
            else:
                print(f"{player_name} has folded.")

        print("==\t\t\t==\n\n\n")

    def advance_phase(self):
        if self.game_phase == PokerStages.PRE_DEAL:
            self.initialize_hands()

        elif self.game_phase == PokerStages.PRE_FLOP:
            self.draw_to_board(3)
            self.game_phase = PokerStages.FLOP

        elif self.game_phase == PokerStages.FLOP:
            self.draw_to_board(1)
            self.game_phase = PokerStages.TURN

        elif self.game_phase == PokerStages.TURN:
            self.draw_to_board(1)
            self.game_phase = PokerStages.RIVER

        elif self.game_phase == PokerStages.RIVER:
            self.winner = self.determine_winner()
            self.game_phase = PokerStages.REVEAL

        if (self.debug):
            self.display_phase()