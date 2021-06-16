import pandas as pd
from .game_reader import GameReader
from .openings import combine_like_openings
from pathlib import Path


class GameLibrary:
    """Reads in all pgns in parent_dir, generates a dataframe of the library with
    summaries of each game as rows."""
    def __init__(self, parent_dir, limit = 2000):
        self.parent_dir = parent_dir
        self.username = parent_dir.split('/')[-1]
        self.df = self.load_library(limit)
    
    def load_library(self, limit):
        """From the parent_dir, loads pgns and their summaries into a dataframe."""
        library = [] 

        library_files = list(Path(self.parent_dir).rglob("*.[tT][xX][tT]"))
        print(f"Loading library ({len(library_files)} files)...") 
        for i, fname in enumerate(library_files[:limit]):
            game = GameReader(str(fname))
            library.append(game.describe())
        print("...loaded.\n")

        library_df = pd.DataFrame(library, columns = ['White', 'Black', 'Result', 'WElo', 'BElo',
                                                        'ECO', 'Opening', 'Date', 'Time', 'id', 'fname'])
        return library_df

    def extract_openings_from_ecourl(self, color=None):
        """Extract opening names found in ECOUrl header."""
        if color is not None:
            sub_df = self.df[self.df[color] == self.username]
        else:
            sub_df = self.df
        eco_urls = sub_df['fname'].apply(lambda x: GameReader(x).headers['ECOUrl'] if 'ECOUrl' in GameReader(x).headers else '').values
        openings = [eco_url.split('/')[-1] for eco_url in eco_urls]
        return openings

    def opening_frequencies(self, color=None):
        """Aggregates opening names from ECOURL, by string similarity, 
        and sums for frequency of main lines."""
        openings = self.extract_openings_from_ecourl(color)
        return combine_like_openings(openings)


    def winrates(self):
        """ Winrates by color"""
        white_df = self.df[self.df['White'] == self.username]
        black_df = self.df[self.df['Black'] == self.username]
        black_wr = len(black_df[black_df['Result']==0])/len(black_df)
        white_wr = len(white_df[white_df['Result']==1])/len(white_df)
        return white_wr, black_wr
    
    # TODO
    # Games by color
    # Winrate
    # Best time control
    # Plot against time
