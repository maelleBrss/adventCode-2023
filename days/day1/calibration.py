import sys
import re
from typing import List

def find_match(list_pattern: List[str], input_string: str) -> List[str]:
    all_matches = []
    for digit_s in list_pattern:
        matches_s = re.finditer(rf'{digit_s}', input_string)
        for m_s in matches_s:
            all_matches.append((m_s.start(), digit_s))
    return all_matches

def compute_calibration_values(input_lines: List[str]) -> None:
    list_all_calibration = []
    list_digit_string = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    for line in lines:
        list_digit = [character for character in line if character.isdigit()]

        matches_string = find_match(list_digit_string, line)
        matches_digit = find_match(list_digit, line)

        sorted_match = sorted(matches_string + matches_digit, key=lambda tup: tup[0])
        first_value = sorted_match[0][1]
        last_value = sorted_match[-1][1]

        if any(c.isalpha() for c in first_value):
            first_value = word_to_number[first_value]
        if any(c.isalpha() for c in last_value):
            last_value = word_to_number[last_value]

        list_all_calibration.append(str(first_value) + str(last_value))

    sum_total = sum(int(calib) for calib in list_all_calibration)
    print(f'sum: {sum_total}')

if __name__ == '__main__':
    word_to_number = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    compute_calibration_values(lines)
