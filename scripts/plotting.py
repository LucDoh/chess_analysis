import matplotlib.pyplot as plt
import sys 
sys.path.append(".")
from chess_analytics.game_library import GameLibrary



if __name__=="__main__":
    # Make game library
    games_dir = sys.argv[1]
    library = GameLibrary(games_dir)
    df = library.df

    
    # Separate into games as white and black
    df_as_white = df[df.White == games_dir.split('/')[-1].capitalize()]
    df_as_black = df[df.Black == games_dir.split('/')[-1].capitalize()]
    print(f"\n{df.columns}")
    print(f"Games played as white: {len(df_as_white)}, as black: {len(df_as_black)} (total: {len(df)})")
    print(df.sample(5))
    # Round ratings to nearest 100
    opp_ratings_as_white = df_as_white.BElo.apply(lambda x: round(int(x)/100)*100).value_counts()
    opp_ratings_as_black = df_as_black.WElo.apply(lambda x: round(int(x)/100)*100).value_counts()

    opp_ratings_as_white.index = opp_ratings_as_white.index.astype(int)
    opp_ratings_as_black.index = opp_ratings_as_black.index.astype(int)

    # Plot the range of opponents ratings
    fig, ax = plt.subplots(2,1)
    opp_ratings_as_white.sort_index().plot.bar(ax=ax[0], label='Opponent rating (black)', color='r', alpha=0.8)
    opp_ratings_as_black.sort_index().plot.bar(ax=ax[0], label='Opponent rating (white)', color='b', alpha=0.5)
    ax[0].set_xlabel("Rating")
    ax[0].set_ylabel("Number")
    ax[0].legend()

    # Bar plot of the top 40 ECO codes played
    df.ECO.value_counts().nlargest(40).plot.bar(ax=ax[1])
    ax[1].set_xlabel("ECO")
    ax[1].set_ylabel("NUmber of games")
    plt.show()

