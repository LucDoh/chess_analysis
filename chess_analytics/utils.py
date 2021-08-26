import os
# Game similarity functions
def jaccard_similarity(moves_1, moves_2):
    """Compares 2 move lists, using Jaccard Similarity."""
    moves_1 = set(moves_1)
    moves_2 = set(moves_2)
    return len(moves_1.intersection(moves_2))/len(moves_1.union(moves_2))
    
def overlap_similarity(moves_1, moves_2):
    """Compares 2 move lists, using overlap similarity."""
    moves_1 = set(moves_1)
    moves_2 = set(moves_2)
    return len(moves_1.intersection(moves_2))/min(len(moves_1), len(moves_2))

def compare_games(game_1, game_2, method='overlap'):
    if method=='overlap':
        return overlap_similarity(game_1.moves, game_2.moves)
    elif method=='jaccard':
        return jaccard_similarity(game_1.moves, game_2.moves)
    else:
        raise Exception("Similarity method not available")


# Position evaluation functions:
from stockfish import Stockfish
import chess.engine
def evaluate_position(fen_board, stockfish_path = '/usr/games/stockfish'):
    """Evaluate a position with chess.engine with a path to stockfish (or another engine),
    position must be in Forsyth–Edwards Notation."""
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    board = chess.Board(fen_board)
    return engine.analyse(board, chess.engine.Limit(depth=20))

def evaluate_position_sf(fen_board, threads=2, depth=2):
    """Evaluate a position using stockfish, position must be in Forsyth–Edwards Notation.
    TODO - Pass arbitrary params, the default depth seems OOL with evaluate_position()"""
    stockfish_engine = Stockfish(parameters={"Threads": threads})
    stockfish_engine.set_fen_position(fen_board)
    return stockfish_engine.get_evaluation()


# Image work  
def position_to_image(fen_position, output_name, filetype="png"):
    """Given a FEN position, save it as an SVG or PNG image to fname."""
    import chess.svg
    import cairosvg
    fname_svg = output_name + ".svg"
    boardsvg = chess.svg.board(board=chess.Board(fen_position))
    with open(fname_svg, "w") as f:
        f.write(boardsvg)
    
    if filetype == "png":
        cairosvg.svg2png(url=fname_svg, write_to=output_name + ".png")
        os.remove(fname_svg)
    

# TODO - Render a board in iPython (create figure)






