import re
import sys
import math
from typing import List
from functools import reduce
import logging


def compute_points(input_lines: List[str]) -> None:
    list_points = []
    for line in input_lines:
        line_without_id = line.split(':')[1][1:]
        # card_id = line.split(':')[0].split()[1]
        list_round = list(map(str.strip, line_without_id.split('|')))
        winning_nb, other_nb = [list(map(int, x.split())) for x in list_round]

        count_points = 0

        if list(set(winning_nb).intersection(other_nb)):
            common_elt = [elt for elt in other_nb if elt in winning_nb]
            count_points = 1 if len(common_elt) == 1 else int(math.pow(2, len(common_elt[1:])))
        list_points.append(count_points)

    print(sum(list_points))


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    compute_points(lines)
