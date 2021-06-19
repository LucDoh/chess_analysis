import pandas as pd
from .game_reader import GameReader
from .openings import combine_like_openings, get_mainline
from pathlib import Path


class GameLibrary:
    """Reads in all pgns in parent_dir, generates a dataframe of the library with
    summaries of each game as rows."""
    def __init__(self, parent_dir, limit = 2000):
        self.parent_dir = parent_dir
        self.username = parent_dir.split('/')[-1]
        self.df = self.load_library(limit)
        self.get_chcom_openings()

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
                                                        'ECO', 'Opening', 'Date', 'TimeControl', 'id', 'fname'])
        return library_df


    def loadin_games(self, limit=5000):
        """ Loads all games into memory, unless above the limit. This increases
        the object size by ~ 10MB/(1000 games). """
        if len(self.df) <= limit:
            self.df['Game'] = self.df.fname.apply(lambda fname: GameReader(fname))
        else:
            self.df['Game'] = None

    def winrates(self):
        """ Winrate by color. """
        white_df = self.df[self.df['White'] == self.username]
        black_df = self.df[self.df['Black'] == self.username]
        black_wr = len(black_df[black_df['Result']==0])/len(black_df)
        white_wr = len(white_df[white_df['Result']==1])/len(white_df)
        return white_wr, black_wr


    def get_chcom_openings(self):
        """Chess.com suggested opening, simplify this to get ~mainlines."""
        self.df['opening_chesscom_spec'] = self.extract_openings_from_ecourl()
        self.df['opening_chesscom_general'] = self.mainline_openings()


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
        and sums their counts to get frequency of main lines."""
        return combine_like_openings(self.df.opening_chesscom_spec)
    

    def mainline_openings(self):
        """Maps specific openings to mainlines, based on mainlines from opening_frequencies()."""
        specific_openings = self.df.opening_chesscom_spec
        mainlines = [x[0] for x in self.opening_frequencies()]
        return [get_mainline(mainlines, opening) for opening in specific_openings]


    def results_by_openings(self, color = 'White'):
        """Returns a mapping between opening: (wins, losses, draws)."""
        games = self.df[self.df[color] == self.username]
        openings = games['opening_chesscom_spec']
        opening_freqs = combine_like_openings(openings)

        # Get results for top openings
        opening_wrs = {}
        for main_op in [x[0] for x in opening_freqs]:
            mask = [main_op in op for op in openings]
            games_op = games[mask]
            if color=="White":   
                opening_wrs[main_op] = (len(games_op[games_op.Result==1]), len(games_op[games_op.Result==0]),
                                        len(games_op[games_op.Result==0.5]))
            else:
                opening_wrs[main_op] = (len(games_op[games_op.Result==0]), len(games_op[games_op.Result==1]),
                                        len(games_op[games_op.Result==0.5]))
                        
        return opening_wrs


    # TODO
    # Longest common sequence of moves
    # Most common ways of losing (time, resignation, mate)
    # Cluster games by opening, or similarity
    # Plot against time, allow filtering on dates
