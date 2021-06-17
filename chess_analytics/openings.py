from collections import defaultdict
import sys

# Utility functions to combine openings (from ECOURL)
def chop_opening_ending(opening):
    """Removes the non-word parts of openings."""
    if (opening.split('-')[-1]).isalpha():
        return opening
    else:
        return chop_opening_ending("-".join(opening.split("-")[:-1]))
    
    
def compress_openings(openings):
    """ Compress openings, such that side-lines and main-lines are combined."""
    openings_compressed = defaultdict(int)
    last_matched = -sys.maxsize
    for i, op in enumerate(openings):
        if i <= last_matched:
            continue
        else:
            openings_compressed[op] += 1
            for j, op_2 in enumerate(openings[i+1:]):
                if op in op_2:
                    openings_compressed[op] += 1
                    last_matched = i + 1 + j
                else:
                    break
    return openings_compressed

    
def combine_like_openings(openings):
    """Chop off the ends of openings and then combine them to get main-line counts."""
    openings = sorted([chop_opening_ending(op) for op in openings if op])
    openings = compress_openings(openings)
    print(len(openings))
    print(sum(openings.values()))

    openings = sorted(openings.items(), key=lambda x: -x[1])
    return openings



def process_opening(x):
    """Processing openings derived from ECO."""
    if '*' in x:
        x = ";".join(x[:-2].split(";"))
        return x if len(x) == 1 else x
    else:
        return x