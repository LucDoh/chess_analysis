import unittest
from stockfish import Stockfish


class TestStockfish(unittest.TestCase):
    # Test stockfish evaluation
    def setUp(self):
        import warnings
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def test_stockfish_initialization(self):
        stockfish_engine = Stockfish()

    def test_stockfish_easy_mate(self):
        # Test that it finds mate in 2
        stockfish_engine = Stockfish("/usr/games/stockfish")
        position_mate_in_two = "r2qb1rk/ppb2p1p/2n1pPp1/B3N3/2B1P2Q/2P2R2/1P4PP/7K w - - 0 1"
        stockfish_engine.set_fen_position(position_mate_in_two)
        proposed_moves = stockfish_engine.get_top_moves()
        self.assertEqual({'Move': 'h4h7', 'Centipawn': None, 'Mate': 2}, proposed_moves[0])
