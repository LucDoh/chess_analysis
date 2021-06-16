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

def plot_openings(library, percent=0.2):
    """Plot most played openings."""
    fig, ax = plt.subplots(2,1)

    opening_freqs = library.opening_frequencies()
    opening_freqs = library.opening_frequencies(color='White')
    opening_freqs = opening_freqs[:int(percent*len(opening_freqs))]
    ax[0].barh([" ".join(o[0].split('-')[:3]) for o in opening_freqs],
           [o[1] for o in opening_freqs])
    for tick in ax[0].get_xticklabels():
        tick.set_rotation(45)
    ax[0].invert_yaxis()
    ax[0].set_title('Most played openings (White)')
    ax[0].set_xlabel('Number of games played')

    opening_freqs = library.opening_frequencies(color='Black')
    opening_freqs = opening_freqs[:int(percent*len(opening_freqs))]
    ax[1].barh([o[0] for o in opening_freqs],
           [o[1] for o in opening_freqs])
    for tick in ax[1].get_xticklabels():
        tick.set_rotation(45)
    ax[1].invert_yaxis()
    ax[1].set_title('Most played openings (Black)')
    ax[1].set_xlabel('Number of games played')
    plt.rcParams.update({'font.size': 22})

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
    df = library.df

    # General win-rate plotting
    plot_rating_distribution(df)

    # Better openings plotting
    plot_openings(library)

    # Plot winrate by color
    plot_wrs(library)
    
