import sys
import json
import pandas as pd
import chess.pgn
import chess.polyglot


class GameReader:
    '''Read games from pgn files.'''
    def __init__(self, fgame):
        self.fgame = fgame
        self.headers, self.game = self.read_game()
        self.winner = self.get_winner()
        self.board = None
        self.date = self.infer_date()
        self.eco_code = self.headers['ECO'] if 'ECO' in self.headers else "NaO"
        self.df_eco = self.load_eco_table()
        self.df_nic = self.load_nic_table()
        self.opening = self.eco_to_nic_opening()
        self.time_control = self.headers['TimeControl'] if 'TimeControl' in self.headers else "NT"

    def read_game(self):
        with open(self.fgame) as pgn_file:
            game = chess.pgn.read_game(pgn_file)
        return game.headers, game

    def get_winner(self):
        '''Single-number representation of winner 1 => white, 0 => black, 0.5 => draw.'''
        result = self.headers['Result'].split("-")[0]
        if len(result) == 1:
            return int(result)
        else:
            return float("0.5")

    def infer_date(self):
        if 'Date' in self.headers:
            return self.headers['Date']  
        else:
            return self.headers['EventDate']

    def load_eco_table(self):
        '''Load the Encyclopedia of Chess Openings into a dataframe (2700+ openings).'''
        df_eco = pd.read_csv("data/ECO.txt", sep='\t', names = ["Name", "Moves", "nq"])
        df_eco = df_eco.reset_index().drop(columns=['nq']).iloc[:-2]
        df_eco.columns = ['ECO', 'Name', 'Moves']
        df_eco['ECO'] = df_eco['ECO'].apply(lambda x: x.rstrip())
        return df_eco

    def load_nic_table(self):
        '''Load the New in Chess key (35 ECOs --> Names).'''
        return pd.read_csv("data/NIC_Key.txt", sep='\t')


    def eco_to_opening(self):
        '''Using the eco table and the game's ECO code, find the opening name.
        Issue: this assumes the first row is the main line, but that's not the case.'''
        if self.eco_code == 'NaO':
            # Not an opening
            return self.eco_code
        else:
            # The name of the main line
            return self.df_eco[self.df_eco['ECO'] == self.eco_code].iloc[0]['Name']

    def eco_to_nic_opening(self):
        '''Use NIC table for opening name.'''
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

    def print_game(self, verbose=False):
        '''Print full PGN text or a summary of it.'''
        if verbose:
            print(self.headers)
            print("Full game:")
            print(self.game)
        else:
            print("Summary:")
            print(self.summarize())
    
    def summarize(self):
        result_map = {0: "Black", 1: "White", 0.5: "Draw"}
        result = result_map[self.get_winner()]

        # PlyCount not available on chess.com
        ply = int(self.headers['PlyCount']) if 'PlyCount' in self.headers else None
        n_moves = int(ply/2) if ply is not None else None
        # chess.com puts date in EndDate
        #date = self.headers['EventDate'] if 'EventDate' in self.headers else self.headers['Date']
        eco = self.headers['ECO'] if 'ECO' in self.headers else "Not An Opening"
        if result == "Draw":
            print(f"Draw between {self.headers['White']} and {self.headers['Black']} in {n_moves} moves ({ply} ply).")
            print(f"General Info: ECO = {eco}, date = {self.date}.")
        else:
            print(f"{result} ({self.headers[result]}) won in {n_moves} moves ({ply} ply).")
            print(f"Date = {self.date}, ECO = {eco}")
            print(f"Opening: {self.opening}")

    def describe(self):
        '''Return an array describing the game.
        [W_player, B_player, result, ECO, opening, time control, loss type, ...]'''
        return [self.headers['White'], self.headers['Black'], self.winner,
                self.headers['WhiteElo'], self.headers['BlackElo'], self.eco_code,
                self.opening, self.date, self.time_control, self.fgame]
        
            

if __name__=="__main__":
    fgame = sys.argv[1] if len(sys.argv) > 1 else None
    game_reader = GameReader(fgame)
    game_reader.print_game(verbose=True)
    
    print(game_reader.get_winner())