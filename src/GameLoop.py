from GameEngine.Player import Player
from GameEngine.GameState import GameState, PokerStages

players = ["P1", "P2"]
game_counter = 10

if __name__ == "__main__":
	for _ in range(game_counter):
		game = GameState(players, debug=False)
		while game.get_phase() != PokerStages.REVEAL:
			game.advance_phase()

		game.display_phase()
		print(f"Winner: {game.winner}")