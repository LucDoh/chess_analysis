import sys 
sys.path.append(".")
import matplotlib.pyplot as plt
import pandas as pd
from chess_analytics.game_library import GameLibrary


def plot_results_by_opening(library, color='White', num = 8):
    """ Compute winrates by opening from a library. """
    results_by_opening = library.results_by_openings(color)
    df_results = pd.DataFrame(results_by_opening).T
    df_results.index = ["-".join(i.split("-")[:3]) for i in df_results.index]
    df_results.columns = ['Win', 'Loss', 'Draw']
    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.set_title(f"Results by opening ({color})")
    ax = df_results.head(num).plot.barh(stacked=True, ax=ax, color=['g', 'crimson', 'grey'])
    for i,lbl in enumerate(ax.patches):
        j = i%num
        total = df_results.iloc[j]['Win'] + df_results.iloc[j]['Loss'] + df_results.iloc[j]['Draw']
        ax.annotate("{:.0f}%".format(lbl.get_width()*100/total), (lbl.get_x()+7, lbl.get_y()+.25),
                    fontsize=9, color='black')
    ax.invert_yaxis()
    ax.legend(fontsize="13")
    ax.set_xlabel("Number of games played")
    plt.show()



def plot_wrs(library):
    """Plot 2 bars, mean to represent white/black winrate."""
    white_wr, black_wr = library.winrates()
    fig, ax = plt.subplots()
    ax.bar(['White'], [white_wr])
    ax.bar(['Black'], [black_wr], color='purple')

    ax.set_title("Win Rate by Color")
    ax.set_ylim(0,1.0)
    plt.show()


def plot_rating_distribution(df):
    # TODO - Refactor...
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
    fig, ax = plt.subplots()
    opp_ratings_as_white.sort_index().plot.bar(ax=ax, label='Opponent rating (black)', color='r', alpha=0.8)
    opp_ratings_as_black.sort_index().plot.bar(ax=ax, label='Opponent rating (white)', color='b', alpha=0.5)
    
    ax.set_ylabel("Number of games")
    ax.tick_params(axis='x', labelrotation=60)
    ax.legend()

    plt.show()

if __name__=="__main__":
    # Make game library
    games_dir = sys.argv[1] # data/user_games/Luc777
    library = GameLibrary(games_dir)

    #plot_rating_distribution(library.df)
    plot_results_by_opening(library)
    # Plot winrate by color
    plot_wrs(library)
    
