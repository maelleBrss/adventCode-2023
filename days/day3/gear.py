import re
import sys
import string
from collections import defaultdict
from typing import List
from functools import reduce
import logging

logger = logging.getLogger(__name__)


def part_numbers(input_lines):

    dict_lines = defaultdict(list)

    for i in range(len(input_lines)):
        symbols_wo_dot = string.punctuation.replace('.', '')
        symbol_matches, digit_matches = [], []

        for symbol in symbols_wo_dot:
            pos_symbols = re.finditer(re.escape(symbol), input_lines[i])
            for pos in pos_symbols:
                symbol_matches.append(((pos.start(), pos.end()), symbol, 'symbol', f'id_{i}'))

        digit_pos = re.finditer(r'\d+', input_lines[i])
        for d_pos in digit_pos:
            digit_matches.append(((d_pos.start(), d_pos.end()), d_pos.group(0), 'digit', f'id_{i}'))

        dict_lines[i] = sorted(symbol_matches + digit_matches, key=lambda tup: tup[0])

    list_part_number = []
    for k in dict_lines.keys():
        if any(elt[2] == 'symbol' for elt in dict_lines[k]) and len(dict_lines[k]) > 1:
            for i in range(len(dict_lines[k])):
                if i != len(dict_lines[k]) - 1:
                    if (dict_lines[k][i][0][1] == dict_lines[k][i + 1][0][0]
                            and any(e[2] == 'symbol' for e in [dict_lines[k][i], dict_lines[k][i + 1]])):
                        if dict_lines[k][i][2] == 'digit':
                            list_part_number.append(dict_lines[k][i])
                        else:
                            list_part_number.append(dict_lines[k][i + 1])

        if k != len(dict_lines.keys()) - 1:
            next_line = dict_lines[k+1]
            for elt in dict_lines[k]:
                for elt_next in next_line:  # too many nested loops
                    if elt[0][0] == elt_next[0][1] or elt[0][1] == elt_next[0][0]:
                        if elt[2] == 'digit':
                            list_part_number.append(elt)
                        if elt_next[2] == 'digit':
                            list_part_number.append(elt_next)
                    if elt_next[2] == 'symbol' and elt[2] == 'digit':
                        if elt[0][0] <= elt_next[0][0] <= elt[0][1]:
                            list_part_number.append(elt)
                    if elt[2] == 'symbol' and elt_next[2] == 'digit':
                        if elt_next[0][0] <= elt[0][0] <= elt_next[0][1]:
                            list_part_number.append(elt_next)

    sum_total = sum(int(part_n[1]) for part_n in set(list(list_part_number)))
    print(sum_total)


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    part_numbers(lines)


