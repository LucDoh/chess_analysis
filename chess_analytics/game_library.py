import pandas as pd
from .game_reader import GameReader
from pathlib import Path


class GameLibrary:
    '''Reads in all pgns in parent_dir, generates a dataframe of the library with
    summaries of each game as rows.'''
    def __init__(self, parent_dir, limit = 2000):
        self.parent_dir = parent_dir
        self.username = parent_dir
        self.df = self.load_library(limit)
    
    def load_library(self, limit):
        '''From the parent_dir, loads pgns and their summaries into a dataframe.'''
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

    # Games by color
    # Winrate
    # Best time control
    # Plot against time
