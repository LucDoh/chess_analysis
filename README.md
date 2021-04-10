# chess_analytics
This project aims to provide high-level analysis of large amounts of chess games, starting with a simple way to download an organized collection of all your chess.com games!

On chess.com, you can analyze individual games with a subscription, and they provide simply statistics to all users such as win-rate by color and highest rated opponent win.

As a player, it'd be great to get a deeper cross-game analysis. For example: breakdown of your wins by opening, loss-type frequencies (checkmate, resignation, out of time), and where you often make mistakes. There's potential for cool visualizations like a heatmap of your average chess position by move, which Grandmaster your opening repertoire is most similiar to, etc. It leans on existing libraries like python-chess and makes use of engines and opening books.

At the moment: 

1. intro_to_python-chess.ipynb - demonstrating how to use python-chess on any PGN (game) and interface with polyglot opening books

2. pgn_downloader.py - a script enabling users to download all their games from chess.com, organized in year/month directories.
    ```
    python pgn_downloader.py username
    ```

3. pgn_reader.py - implements a GameReader class to work with PGNs