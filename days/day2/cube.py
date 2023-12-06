import sys
from collections import defaultdict
from typing import List
from functools import reduce


def nb_cubes_higher(color: str, dict_cubes: dict) -> bool:
    return dict_cubes[color] > original_bag[color]

def compute_games(input_lines: List[str]) -> List[tuple]:
    list_games = []

    for line in input_lines:
        line_without_id = line.split(':')[1][1:]
        game_id = line.split(':')[0].split()[1]
        list_round = list(map(str.strip, line_without_id.split(';')))

        for round in list_round:
            dict_cube_round = defaultdict(int)
            split_cubes = list(map(str.strip, round.split(',')))
            game_possible = False
            for cube in split_cubes:
                split_info = cube.split()
                dict_cube_round[split_info[1]] = int(split_info[0])

            if nb_cubes_higher('red', dict_cube_round):
                break
            elif nb_cubes_higher('blue', dict_cube_round):
                break
            elif nb_cubes_higher('green', dict_cube_round):
                break
            else:
                game_possible = True

        if game_possible:
            list_games.append((game_id, True))
        else:
            list_games.append((game_id, False))

    return list_games


def min_cubes(input_lines: List[str]) -> None:
    # don't mind the duplicate code for now
    list_powers = []

    for line in input_lines:
        line_without_id = line.split(':')[1][1:]
        list_round = list(map(str.strip, line_without_id.split(';')))

        list_dict = []
        for round in list_round:
            dict_cube_round = defaultdict(int)
            split_cubes = list(map(str.strip, round.split(',')))
            for cube in split_cubes:
                split_info = cube.split()
                dict_cube_round[split_info[1]] = int(split_info[0])
            list_dict.append(dict_cube_round)

        list_max_value = [max(list_dict, key=lambda x: x[col])[col]
                          for col in original_bag.keys()]

        power_values = reduce(lambda x, y: x * y, list_max_value)
        list_powers.append(power_values)

    sum_total = sum(int(power) for power in list_powers)
    print(sum_total)

def guess_nb_cubes(input_lines: List[str]) -> None:
    list_all_games = compute_games(input_lines)
    list_possible_games = list(filter(lambda g: g[1], list_all_games))
    sum_id = sum(int(game[0]) for game in list_possible_games)
    print(sum_id)



def cube_conundrum(input_lines: List[str]) -> None:
    guess_nb_cubes(input_lines)
    min_cubes(input_lines)


if __name__ == '__main__':
    global original_bag
    original_bag = {'red': 12, 'green': 13, 'blue': 14}

    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    cube_conundrum(lines)

