import re
import sys
import string
from collections import defaultdict
from typing import List
from functools import reduce
import logging

logger = logging.getLogger(__name__)


def get_symbols_digits(input_lines: List[str]) -> dict:
    output_dict = defaultdict(list)
    for i in range(len(input_lines)):
        symbols_wo_dot = string.punctuation.replace('.', '')
        symbol_matches, digit_matches = [], []

        for symbol in symbols_wo_dot:
            pos_symbols = re.finditer(re.escape(symbol), input_lines[i])
            for pos in pos_symbols:
                symbol_matches.append(((pos.start(), pos.end()), symbol, 'symbol', int(i)))

        digit_pos = re.finditer(r'\d+', input_lines[i])
        for d_pos in digit_pos:
            digit_matches.append(((d_pos.start(), d_pos.end()), d_pos.group(0), 'digit', int(i)))

        output_dict[i] = sorted(symbol_matches + digit_matches, key=lambda tup: tup[0])

    return output_dict


def get_simple_part_numbers(input_dict: dict) -> List[tuple]:
    list_part_number = []
    ranges_overlap = lambda r1, r2: not (r1[1] < r2[0] or r1[0] > r2[1])

    for k in input_dict.keys():
        if any(elt[2] == 'symbol' for elt in input_dict[k]) and len(input_dict[k]) > 1:
            for i in range(len(input_dict[k])):
                if i != len(input_dict[k]) - 1:
                    if (input_dict[k][i][0][1] == input_dict[k][i + 1][0][0]
                            and any(e[2] == 'symbol' for e in [input_dict[k][i], input_dict[k][i + 1]])):
                        if input_dict[k][i][2] == 'digit':
                            list_part_number.append(input_dict[k][i])
                        else:
                            list_part_number.append(input_dict[k][i + 1])

        if k != len(input_dict.keys()) - 1:
            next_line = input_dict[k + 1]
            for elt in input_dict[k]:
                for elt_next in next_line:  # too many nested loops
                    if elt[0][0] == elt_next[0][1] or elt[0][1] == elt_next[0][0]:
                        if elt[2] == 'digit':
                            list_part_number.append(elt)
                        if elt_next[2] == 'digit':
                            list_part_number.append(elt_next)
                    if elt_next[2] == 'symbol' and elt[2] == 'digit':
                        if ranges_overlap(elt[0], elt_next[0]):
                            list_part_number.append(elt)
                    if elt[2] == 'symbol' and elt_next[2] == 'digit':
                        if ranges_overlap(elt[0], elt_next[0]):
                            list_part_number.append(elt_next)
    return list_part_number


def get_gear(dict_input: dict) -> dict:
    dict_gear = {}

    for k in range(len(dict_input.keys())):
        curr_line = dict_input[k]
        prev_line = dict_input[k - 1] if k != 0 else []
        next_line = dict_input[k + 1] if k != len(dict_input.keys()) - 1 else []
        ranges_overlap = lambda r1, r2: not (r1[1] < r2[0] or r1[0] > r2[1])

        if any(elt[2] == 'symbol' for elt in curr_line):
            for i in range(len(curr_line)):
                elt = curr_line[i]
                if i != len(curr_line) - 1:
                    if (elt[0][1] == curr_line[i + 1][0][0]
                            and any(e[2] == 'symbol' for e in [elt, curr_line[i + 1]])):
                        potential_gear, potential_digit = (elt, curr_line[i + 1]) if elt[2] == 'symbol' else (
                            curr_line[i + 1], elt)
                        dict_gear[potential_gear] = dict_gear[potential_gear] + [
                            potential_digit] if potential_gear in dict_gear else [potential_digit]

                if elt[2] == 'symbol':
                    if next_line:
                        for elt_next in next_line:
                            if ranges_overlap(elt[0], elt_next[0]):
                                dict_gear[elt] = dict_gear[elt] + [elt_next] if elt in dict_gear else [elt_next]
                    if prev_line:
                        for elt_prev in prev_line:
                            if ranges_overlap(elt[0], elt_prev[0]):
                                dict_gear[elt] = dict_gear[elt] + [elt_prev] if elt in dict_gear else [elt_prev]

    return dict_gear


def part_numbers(input_lines: List[str]) -> None:
    dict_lines = get_symbols_digits(input_lines)
    list_part_n = get_simple_part_numbers(dict_lines)
    sum_total = sum(int(part_n[1]) for part_n in set(list(list_part_n)))

    print(sum_total)


def gear_ratio(input_lines: List[str]) -> None:
    dict_lines = get_symbols_digits(input_lines)
    dict_gear = {key: [tup for tup in value if tup[1] == '*' or tup[2] == 'digit']
                 for key, value in dict_lines.items()}
    dict_gears = get_gear(dict_gear)

    list_ratio = []
    for key, value in dict_gears.items():
        dict_gears[key] = set(list(value))
        if len(dict_gears[key]) >= 2:
            list_ratio.append(reduce(lambda x, y: x * y, [int(v[1]) for v in dict_gears[key]]))

    print(sum(list_ratio))


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    part_numbers(lines)
    gear_ratio(lines)
