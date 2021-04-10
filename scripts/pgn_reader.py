import sys
import json
import chess.pgn
import chess.polyglot

class GameReader:
    def __init__(self, fgame):
        self.fgame = fgame
        self.headers, self.game = self.get_game()
        self.winner = self.get_winner()
        self.board = None

    def get_game(self):
        with open(self.fgame) as pgn_file:
            game = chess.pgn.read_game(pgn_file)
        return game.headers, game

    def get_winner(self):
        # 1 --> win, 0 --> loss, 1/2 --> draw
        result = self.headers['Result'].split("-")[0]
        if len(result) == 1:
            return int(result)
        else: # it's a draw
            return float("0.5")
        
    def print_game(self, ):
        print(self.headers)
        print("Full game:")
        print(self.game)
    

if __name__=="__main__":
    fgame = sys.argv[1] if len(sys.argv) > 1 else None
    game_reader = GameReader(fgame)
    game_reader.print_game()
    print(game_reader.get_winner())