from Deck import Deck
from Card import Card
from HandEvaluator import HandEvaluator
from typing import List, Dict
from enum import Enum
from Player import Player

class PokerStages(Enum):
    PRE_DEAL = 0
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    REVEAL = 5

class GameState:
    def __init__(self, players: List[str]):
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

    def initialize_hands(self):
        for _ in range(2):
            for player_name, player_obj in self.players.items():
                if player_obj.get_status():
                    player_obj.add_card(self.deck.draw_card())

        self.game_phase = PokerStages.PRE_FLOP

    def draw_to_board(self, count: int):
        for _ in range(count):
            self.board.append(self.deck.draw_card())

    def determine_winner(self) -> str:
        best_hand = None
        best_strength = [-1, -1]
        winner = None

        for player_name, player_obj in self.players.items():
            if not player_obj.get_status():
                continue

            evaluator = HandEvaluator(player_obj.get_cards(), self.board)
            strength = evaluator.evaluate_hand()

            if strength[0] > best_strength[0] or (strength[0] == best_strength[0] and strength[1] > best_strength[1]):
                best_strength = strength
                best_hand = evaluator
                winner = player_name

        return winner

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