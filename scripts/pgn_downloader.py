import sys
import urllib.request
import json 

class GameDownloader:
    ''' Download all games played on a chess.com for a user.
    References: 
    - chess.com/news/view/published-data-api#pubapi-endpoint-games-pgn
    - chess.com/forum/view/suggestions/export-all-my-games-to-my-personal-database
    '''
    def __init__(self, username):
        self.username = username
        self.dates = []
        self.games = []
    
    def get_dates(self):
        # Find all month/year combos that the user played on
        # api.chess.com/pub/player/{username}/games/archives
        # Returns JSON of { "archives": [".../{user}/games/2009/10", ...] }
        archive_url = f'https://api.chess.com/pub/player/{self.username}/games/archives'
        with urllib.request.urlopen(archive_url) as url:
            content = json.loads(url.read().decode())
        self.dates = [c.split('/')[-2:] for c in content['archives']]
    
    def get_games(self, limit = None, specify_dates = None):
        # For a year/month: https://api.chess.com/pub/player/{user}/games/2009/10/pgn
        # Games are separated by blank lines
        pgns = []
        dates = specify_dates if specify_dates else self.dates[:limit]
        for year, month in dates:
            games_url = f'https://api.chess.com/pub/player/{self.username}/games/{year}/{month}/pgn'
            with urllib.request.urlopen(games_url) as url:
                content = url.read().decode()
                pgns.extend(content.split('\n\n\n')) # Games are separated by two blank lines

        print(f"Got {len(pgns)} games!")
        self.games = pgns
    
    def games_to_file(self, fname):
        with open(fname, 'w') as f:
            for game in self.games:
                f.write(game + '\n\n\n')
        print(f"Wrote to {fname}")
            
def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
        game_downloader = GameDownloader(username)
        game_downloader.get_dates()
        pgns = game_downloader.get_games() 
        game_downloader.games_to_file(f"../data/all_{username}_games.txt")
    else:
        print("No username provided...")

if __name__=="__main__":
    main()
