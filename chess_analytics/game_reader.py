import sys
import json
from functools import lru_cache
import re
import pandas as pd
import chess.pgn
import chess.polyglot


class GameReader:
    """Read games from pgn files."""
    def __init__(self, fgame):
        self.fgame = fgame
        self.game, self.headers = self.read_game()
        self.pgn = self.parse_pgn()
        self.moves = self.parse_moves()
        self.result = self.get_result()
        self.date = self.infer_date()
        self.eco_code = self.headers['ECO'] if 'ECO' in self.headers else "NaO"
        self.time_control = self.headers['TimeControl'] if 'TimeControl' in self.headers else "NT"
        self.df_eco = self.load_eco_table()
        self.df_nic = self.load_nic_table()
        self.opening = self.eco_to_nic_opening()

    def __eq__(self, other):
        """If two games have the same pgn (including headers), they're the same game."""
        return str(self.game) == str(other.game)

    
    @classmethod
    @lru_cache(maxsize=None)
    def load_eco_table(cls):
        """Load Encyclopedia of Chess Openings into dataframe (2700+ openings)."""
        df_eco = pd.read_csv("data/ECO.txt", sep='\t', names = ["Name", "Moves", "nq"])
        df_eco = df_eco.reset_index().drop(columns=['nq']).iloc[:-2]
        df_eco.columns = ['ECO', 'Name', 'Moves']
        df_eco['ECO'] = df_eco['ECO'].apply(lambda x: x.rstrip())
        return df_eco

    @classmethod
    @lru_cache(maxsize=None)
    def load_nic_table(self):
        """Load New in Chess key (35 ECOs --> Names)."""
        return pd.read_csv("data/NIC_Key.txt", sep='\t')

    def __str__(self):
        return self.pgn

    def read_game(self):
        """Returns headers, python-chess' game object, and the PGN string. """
        with open(self.fgame) as pgn_file:
            game = chess.pgn.read_game(pgn_file)
        return game, game.headers


    # Openings
    def eco_to_opening(self):
        """Using the eco table + game's ECO code, find the opening name.
        Issue: this assumes the first row is the main line, but that's not the case."""
        if self.eco_code == 'NaO':
            return self.eco_code
        else:
            # Lookup main line name
            return self.df_eco[self.df_eco['ECO'] == self.eco_code].iloc[0]['Name']

    def eco_to_nic_opening(self):
        """Use NIC table for opening name."""
        if self.eco_code == 'NaO': # Not an opening
            return self.eco_code

        # Direct match
        match = self.df_nic.Name[self.df_nic['Codes'] == self.eco_code]
        if match.size > 0:
            return match.values[0]
        else:
            # Get from code_range
            letter, code_int = self.eco_code[0], int(self.eco_code[1:])
            for i, code_range in enumerate(self.df_nic.Code_ranges.values):
                if (letter == code_range[0]) and (code_int >= code_range[1]) and (code_int <= code_range[2]):
                    return self.df_nic.Name.iloc[i].rstrip()
            
            # If missing, fall back on data/ECO.txt
            # (e.g the Philidor Defense)
            return self.eco_to_opening() + "*"
    
    def clean_pgn(self):
        """ Scrubs comments, side-lines and move-numbers from PGN. """
        clean_pgn = ""
        is_dirty = False
        for x in self.pgn:
            if x =="{":
                is_dirty = True
            elif x == "}":
                is_dirty = False
            else:
                if not is_dirty:
                    clean_pgn += x
        
        # Remove redundant move-numbers (1...) and result
        clean_pgn = re.sub('\d{1,2}[.]{3} ', '', clean_pgn) 
        return " ".join([p for p in clean_pgn.split(' ')[:-1] if p !=""])


    def parse_pgn(self):
        """Parses and cleans the pgn, removing comments, side-lines, result. """
        self.pgn = str(self.game).split('\n\n')[1] # 0 is headers, 1 is the moves
        return self.clean_pgn()


    def parse_moves(self):
        """ Parse moves from pgn, returns either i) two separate arrays for B/W or ii) one list,
        e.g. ['e4', 'e5', 'Nf3', 'Nf6', ...]."""
        moves = self.pgn.split(" ")
        del moves[::3] # Remove move numbers
        return moves # moves_white, moves_black = moves[0::2], moves[1::2]  

    def play_nth_move(self, n=1):
        """Play n plys using python-chess game object, return new board state. In Jupyter, this renders
        an image of the board."""
        board = self.game.board()
        moves = list(self.game.mainline_moves())
        for move in moves[:n]:
            board.push(move)
        return board
    
    def get_result(self):
        """Single-number representation of winner 1 => white, 0 => black, 0.5 => draw."""
        result = self.headers['Result'].split("-")[0]
        return int(result) if len(result) == 1 else float("0.5")


    def infer_date(self):
        if 'Date' in self.headers:
            return self.headers['Date']  
        else:
            return self.headers['EventDate']

    def print_game(self, verbose=False):
        """ Print full PGN text or summarize it."""
        if verbose:
            print("Full game:")
            print(self.headers)
            print(self.game)
        else:
            print("Summary:")
            print(self.summarize())
    

    def summarize(self):
        result_map = {0: "Black", 1: "White", 0.5: "Draw"}
        result = result_map[self.get_result()]

        # PlyCount not available on chess.com
        ply = int(self.headers['PlyCount']) if 'PlyCount' in self.headers else None
        n_moves = int(ply/2) if ply is not None else None
        eco = self.headers['ECO'] if 'ECO' in self.headers else "NoA"
        if result == "Draw":
            print(f"Draw between {self.headers['White']} and {self.headers['Black']} in {n_moves} moves ({ply} ply).")
            print(f"General Info: ECO = {eco}, date = {self.date}.")
        else:
            print(f"{result} ({self.headers[result]}) won in {n_moves} moves ({ply} ply).")
            print(f"Date = {self.date}, ECO = {eco}")
            print(f"Opening: {self.opening}")

    def describe(self):
        """Return an array describing the game.
        [W_player, B_player, result, ECO, opening, time control, loss type, ...]"""
        return [self.headers['White'], self.headers['Black'], self.result,
                self.headers['WhiteElo'], self.headers['BlackElo'], self.eco_code,
                self.opening, self.date, self.time_control, self.headers['Link'],
                self.fgame]
        
            

if __name__=="__main__":
    fgame = sys.argv[1] if len(sys.argv) > 1 else None
    game_reader = GameReader(fgame)
    game_reader.print_game(verbose=True)
    
    print(game_reader.get_result())