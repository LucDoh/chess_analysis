# Tactics
import random
import chess
from stockfish import Stockfish
import chess.engine

def find_forced_mate(game, stockfish_engine, mate_in=2, extra_description=""):
    """Given a GameReader object, return (fen_position, description, link) of the first
    forced mate in the game."""
    for j in range(len(game.moves)):
    # Find first Mate in 2 and break
        board = game.play_nth_move(j)
        stockfish_engine.set_fen_position(board.fen())
        proposed_moves = stockfish_engine.get_top_moves()
        if proposed_moves[0]['Mate'] == mate_in:
            describer = game.describe()
            description = f"{describer[0]} vs. {describer[1]} ({describer[2]}) {extra_description}"
            return (board.fen(), description, describer[9])
    return (None, None, None)

def find_forced_mate_positions(library, mate_in = 2, limit=100):
    """Finds up to limit forced mates and returns the FEN position + description."""
    stockfish_engine = Stockfish("/usr/games/stockfish")
    forced_mate_boards = []
    for i, game in enumerate(library.df.Game.values):
        # For everygame...
        if len(forced_mate_boards) == limit:
            break
        forced_mate_tuple = find_forced_mate(game, stockfish_engine, extra_description=f"[{library.df.iloc[i]['opening_chesscom_general']}]")
        if forced_mate_tuple[0] is not None:
            forced_mate_boards.append(forced_mate_tuple)
    return forced_mate_boards

def render_tactic(tactic_data):
    """Renders a board with tactic and prints extra information."""
    print(tactic_data[1])
    print(tactic_data[2])
    print(f"{tactic_data[0].split()[1].upper()}, Move {tactic_data[0].split()[-1].upper()}")
    return chess.Board(tactic_data[0])
    
def render_random_tactic(tactics_data):
    """Tactics data is a list of (fen_position, description, link."""
    rnd = random.randint(0,len(tactics_data))
    return render_tactic(tactics_data[rnd])