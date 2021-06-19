# chess_analytics
### What for?
This project aims to give a high-level analysis of large amounts of chess games, starting with a simple way to download an organized collection of all your Chess.com games! 

Players can view simple statistics about their games on Chess.com, like win-rate by color and best win. They can also analyze a couple games per day for free. This package aims to go a bit further, without requiring additional work from the player.

Examples:
- winrate by opening 
- opening distribution 

Future features:
- loss-type frequencies (checkmate, resignation, out of time)
- suggest grandmasters with similar repertoires
- visualizations: show moves which are often mistakes (go down in EV), and heatmap of positions by move

### Components

1. **notebooks/intro_to_python-chess.ipynb** -  working with PGNS using python-chess and interfacing with polyglot opening books.

2. **scripts/pgn_downloader.py** - download Chess.com games for a user, organized in year/month directories.
    ```
    python scripts/pgn_downloader.py username
    ```

3. **chess_analytics/game_reader.py** - implements GameReader, a class to work with PGNs.

4. **chess_analytics/game_library.py** - build a library of games from a directory, represented as a dataframe with 1 row per game.
    ```
    from chess_analytics.game_library import GameLibrary
    library = GameLibrary("data/user_games/user/")
    print(len(library.df))
    ```
    ```
    >> 1969
    ```
    ```
    library.df.head()
    ```
    ![Sample of dataframe](data/figures/df_sampled.png)

5. **scripts/plotting.py** - visualize a library of games - opponent rating distribution, winrate by opening, opening distribution.
<p align="center">
    <img src="data/figures/Rating_distribution.png" width="360"/>
    <img src="data/figures/Winrate_by_opening_white.png" width="330"/>
</p>

### Sources

- [python-chess](https://python-chess.readthedocs.io/en/latest/#)
- [Chess.com API](https://www.chess.com/club/chess-com-developer-community)
- [Opera Game PGN](https://www.chessgames.com/perl/chessgame?gid=1233404) (Paul Morphy vs. Duke of Brunswick and Count Isouard, 1958)
- [Polyglot opening book](https://github.com/niklasf/python-chess/raw/master/data/polyglot/performance.bin)
- [Encyclopedia of Chess Openings](https://github.com/seberg/icsbot/blob/master/misc/eco.txt)