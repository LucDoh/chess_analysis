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
        library = [] # pd.DataFrame()
        library_files = list(Path(self.parent_dir).rglob("*.[tT][xX][tT]"))
        for i, fname in enumerate(library_files[:limit]):
            print(f"{i}.", end='') 
            game = GameReader(str(fname))
            library.append(game.describe())

        library_df = pd.DataFrame(library, columns = ['White', 'Black', 'Result', 'WElo', 'BElo',
                                                        'ECO', 'Opening', 'Date', 'Time', 'fname'])
        return library_df
