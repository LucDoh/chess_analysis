import sys
import urllib.request
import json 
from pathlib import Path


class GameDownloader:
    """ Download all games played on a chess.com for a user. See: 
    - chess.com/news/view/published-data-api#pubapi-endpoint-games-pgn
    - chess.com/forum/view/suggestions/export-all-my-games-to-my-personal-database
    """
    def __init__(self, username):
        self.username = username
        self.dates =  self.get_dates()
        self.games = []
        
    
    def get_dates(self):
        """Find all month/year combos that the user played through a request to
        api.chess.com/pub/player/{username}/games/archives, which returns JSON:
        { "archives": [".../{user}/games/2009/10", ...] }"""
        archive_url = f'https://api.chess.com/pub/player/{self.username}/games/archives'
        with urllib.request.urlopen(archive_url) as url:
            content = json.loads(url.read().decode())
        return [c.split('/')[-2:] for c in content['archives']]
    
    def download_games(self, limit = None, specify_dates = None):
        """By year/month: https://api.chess.com/pub/player/{user}/games/2009/10/pgn
        (games are separated by 3 blank lines)."""
        pgns = {}
        dates = specify_dates if specify_dates else self.dates[:limit]
        for year, month in dates:
            games_url = f'https://api.chess.com/pub/player/{self.username}/games/{year}/{month}/pgn'
            with urllib.request.urlopen(games_url) as url:
                content = url.read().decode()
                pgns[(year, month)] = content.split('\n\n\n') # Dictionary indexed by (year, month)

        print(f"Got {sum([len(games_my) for games_my in pgns.values()])} games!")
        self.games = pgns
    
    def games_to_file(self, fname):
        """Stores all games into one long text file, split by two blank lines"""
        with open(fname, 'w') as f: 
            for k, games in self.games.items():
                for game in games:
                    f.write(game + '\n\n\n')
        print(f"Wrote to {fname}")

    def games_to_folder(self, foldername = None):
        """Store games in a directory with subdirectories by year and month."""

        foldername = foldername if foldername else self.username
        full_path = f"data/user_games/{foldername}"
        Path(full_path).mkdir(parents=True, exist_ok=True)
        print(f"Writing to {full_path}")

        for d in self.dates:
            # year/month subdirectories
            subdirectory_path = f"data/user_games/{foldername}/{d[0]}/{d[1]}/"
            Path(subdirectory_path).mkdir(parents=True, exist_ok=True)
            for i, g in enumerate(self.games[tuple(d)]):
                gamename = f"{subdirectory_path}game_{i}.txt"

                with open(gamename, 'w') as f:
                    f.write(g)


def main():
    """ Given a chess.com username, fetch all games played. """
    if len(sys.argv) > 1:
        username = sys.argv[1]
        game_downloader = GameDownloader(username)
        game_downloader.download_games() 
        game_downloader.games_to_folder()

    else:
        print("No username provided...")

if __name__=="__main__":
    main()
