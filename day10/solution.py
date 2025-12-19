#!/usr/bin/env python3

import logging
import os
from functools import reduce
from itertools import combinations

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    """Read the input file and return its contents as a string."""
    with open(fn, encoding='utf-8') as f:
        data = f.read()
    return data

def parse_data(text_data):
    """Parse the input data and return as data ready for processing."""
    line_parts = [line.split() for line in text_data.strip('\n ').split('\n')]
    entries = []
    for parts in line_parts:
        objective_text = ['0' if c == '.' else '1' for c in parts[0].strip('[]')]
        objective_text.reverse()
        objective = int(''.join(objective_text), 2)
        buttons = []
        for button_text in parts[1:-1]:
            button_bits = [int(x) for x in button_text.strip('()').split(',')]
            button = reduce(lambda x, y: x + 2 ** y, button_bits, 0)
            buttons.append(button)
        joltages = [int(x) for x in parts[-1].strip('{}').split(',')]
        entry = {
            'objective': objective,
            'buttons': buttons,
            'joltages': joltages
        }
        entries.append(entry)
    return entries

def get_part1_solution(parsed_data):
    """Complete Part 1 solution here"""
    total_min_presses = 0
    for entry in parsed_data:
        objective = entry['objective']
        buttons = entry['buttons']
        min_presses = None
        for buttons_pressed in range(1, len(buttons) + 1):
            # get each combination of presses for num_presses
            if min_presses is None:
                for combo in combinations(buttons, buttons_pressed):
                    combo_xor = reduce(lambda x, y: x ^ y, combo, 0)
                    if combo_xor == objective:
                        logger.debug(msg=f"for button {objective} found minimum {buttons_pressed} with combo {combo}")
                        min_presses = buttons_pressed
                        break
        total_min_presses += min_presses
    return total_min_presses

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    return None

def print_answer(answer, part=1):
    """Print the answer in a standard format."""
    dirname = os.path.basename(os.getcwd())
    if dirname.startswith('day'):
        print(f"Day {int(dirname[3:])} Part {part} Answer: {answer}")
    else:
        print(f"Part {part} Answer: {answer}")

def main():
    """Main function to run the solution."""
    data = get_file_data()
    parsed_data = parse_data(data)
    answer = get_part1_solution(parsed_data)
    print_answer(answer, part=1)
    answer = get_part2_solution(parsed_data)
    print_answer(answer, part=2)

if __name__ == '__main__':
    main()
