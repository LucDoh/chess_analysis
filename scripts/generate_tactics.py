import sys
import json
import argparse
sys.path.append(".")
from chess_analytics.game_library import GameLibrary
from chess_analytics.utils import position_to_image

""" Tactics Generator: From a library of pgns, automatically find and
generate tactics and output them as PNGs."""
OUTPUT_DIR = "data/output/tactics/"


def tactics_to_json(tactics_data, output_name):
    tactics_dict = [{'link': link, 'description': descrip, 'position': pos} for (pos, descrip, link) in tactics_data]
    with open(output_name, 'w') as f:
        json.dump(tactics_dict, f, indent=4)

def generate_tactics_pngs(tactics_data, output_dir):
    for tactic_data in tactics_data:
        image_name = f"{'_'.join(tactic_data[1].split()[:3])}_{tactic_data[0].split()[1]}_to_move"
        image_name = f"{output_dir}" + image_name
        position_to_image(tactic_data[0], image_name, filetype="png")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', type=str)
    parser.add_argument('-limit', type=int, default=10)
    parser.add_argument('-output', type=str, default=OUTPUT_DIR)
    parser.add_argument('-no_images', default=False, action='store_true')
    parser.add_argument('-mate', default=2)
    args = parser.parse_args()
    # 1) Build a library from the directory
    games_directory = args.input
    library = GameLibrary(games_directory)
    print(f"Number of games = {len(library)}")
    # 2) Generate tactics (mate-in-twos)
    tactics_data = library.find_mate_positions(limit=args.limit, mate_in=args.mate)
    print(f"Number of tactics = {len(tactics_data)}")
    # 3) Output tactics as JSON
    output_name = args.output + f"{len(tactics_data)}_tactics.json"
    tactics_to_json(tactics_data, output_name)
    # 4) Generate tactics pngs 
    if not args.no_images:
        generate_tactics_pngs(tactics_data, args.output)

if __name__=="__main__":
    main()