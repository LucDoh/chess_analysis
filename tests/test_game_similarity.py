import unittest
from unittest.mock import Mock
from chess_analytics.game_reader import GameReader
from chess_analytics.utils import overlap_similarity, jaccard_similarity, compare_games
class TestGameSimilarity(unittest.TestCase):
    moves_1 = ['e4']
    moves_2 = ['e5']
    moves_3 = ['e4', 'e5', 'd4', 'exd4']
    moves_4 = ['e4', 'e5', 'd4', 'd6']
    def test_overlap_similarity(self):
        similarity_a = overlap_similarity(self.moves_1, self.moves_2)
        similarity_b = overlap_similarity(self.moves_1, self.moves_1)
        similarity_c = overlap_similarity(self.moves_3, self.moves_4)
        self.assertEqual(0, similarity_a)
        self.assertEqual(1, similarity_b)
        self.assertEqual(0.75, similarity_c)

    def test_jaccard_similarity(self):
        similarity_a = jaccard_similarity(self.moves_1, self.moves_2)
        similarity_b = jaccard_similarity(self.moves_1, self.moves_1)
        similarity_c = jaccard_similarity(self.moves_3, self.moves_4)
        self.assertEqual(0, similarity_a)
        self.assertEqual(1, similarity_b)
        self.assertEqual(0.60, similarity_c)

    def test_game_similarity(self):
        game_a = Mock()
        game_b = Mock()
        game_a.moves = self.moves_3
        game_b.moves = self.moves_4
        self.assertEqual(0.75, compare_games(game_a, game_b))