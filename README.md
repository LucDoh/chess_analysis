# chess_analytics
### What for?
This project aims to provide high-level analysis of large amounts of chess games, starting with a simple way to download an organized collection of all your chess.com games!

On chess.com, players can view simple statistics about their games, like win-rate by color and best win. They can also analyze a couple games per day for free. This tool tries to fill between those two extremes, by giving you deeper and more specific statistics across games. 

Examples: 
- breakdown of your wins by opening
- loss-type frequencies (checkmate, resignation, out of time)
- nice visualizations, e.g. a heatmap of the user's chess position by move 
- grandmasters that your repertoire is most similiar to, so you can study them

### Components

1. **notebooks/intro_to_python-chess.ipynb** - demonstrates how to use python-chess with any PGN (game) and interface with polyglot opening books.

2. **scripts/pgn_downloader.py** - a script to download all chess.com games for a user, organized in year/month directories.
    ```
    python scripts/pgn_downloader.py username
    ```

3. **chess_analytics/game_reader.py** - implements a GameReader class to work with PGNs.

4. **chess_analytics/game_library.py** - create a library of games from a directory, represented as a dataframe with a row per game.
    ```
    from chess_analytics.game_library import GameLibrary
    library = GameLibrary("data/user_games/username/")
    print(len(library.df))
    ```
    ```
    >> 1969
    ```
    ```
    library.df.head()
    ```
    ![image_name](notebooks/df_sampled.png)

    
### Sources

- [python-chess](https://python-chess.readthedocs.io/en/latest/#)
- [Opera Game PGN](https://www.chessgames.com/pgn/morphy_duke_karl_count_isouard_1858.pgn?gid=1233404) (Paul Morphy vs. Duke of Brunswick and Count Isouard, 1958)
- [Polyglot opening book](https://github.com/niklasf/python-chess/raw/master/data/polyglot/performance.bin)
- [Encyclopedia of Chess Openings](https://github.com/seberg/icsbot/blob/master/misc/eco.txt)