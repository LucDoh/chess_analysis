import matplotlib.pyplot as plt
import sys 
sys.path.append(".")
from chess_analytics.game_library import GameLibrary


def process_opening(x):
    # Keep only descriptive part of name
    if '*' in x:
        x = ";".join(x[:-2].split(";"))
        return x if len(x) == 1 else x
    else:
        return x


if __name__=="__main__":
    # Make game library
    games_dir = sys.argv[1]
    library = GameLibrary(games_dir)
    df = library.df
    
    # Separate into games as white and black
    df_as_white = df[df.White == games_dir.split('/')[-1].capitalize()]
    df_as_black = df[df.Black == games_dir.split('/')[-1].capitalize()]
    print(f"Games played: {len(df)} (W: {len(df_as_white)}, B: {len(df_as_black)})")
    print(f"Sample: \n {df.sample(2)}\n")

    # Round ratings to nearest 100
    opp_ratings_as_white = df_as_white.BElo.apply(lambda x: round(int(x)/100)*100).value_counts()
    opp_ratings_as_black = df_as_black.WElo.apply(lambda x: round(int(x)/100)*100).value_counts()
    opp_ratings_as_white.index = opp_ratings_as_white.index.astype(int)
    opp_ratings_as_black.index = opp_ratings_as_black.index.astype(int)

    # Plot the range of opponents ratings
    fig, ax = plt.subplots(2,1, figsize = (6,8))
    opp_ratings_as_white.sort_index().plot.bar(ax=ax[0], label='Opponent rating (black)', color='r', alpha=0.8)
    opp_ratings_as_black.sort_index().plot.bar(ax=ax[0], label='Opponent rating (white)', color='b', alpha=0.5)
    ax[0].set_ylabel("Number of games")
    ax[0].tick_params(axis='x', labelrotation=60)
    ax[0].legend()

    # Bar plot of the top 10 ECO codes played
    #df.ECO.value_counts().nlargest(10).plot.bar(ax=ax[1])
    #ax[1].set_ylabel("Number of games")

    # Bar plot of the top 10 named openings played
    df['Processed_Opening'] = df['Opening'].apply(lambda x: process_opening(x))
    print(f"Top 5 openings:\n{df.Processed_Opening.value_counts().nlargest(5)}")
    
    df.Processed_Opening.value_counts().nlargest(10).plot.bar(ax=ax[1])
    ax[1].set_ylabel("Number of games")
    ax[1].tick_params(axis='x', labelrotation=35)
    plt.show()

