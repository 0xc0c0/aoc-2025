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

def get_binary_from_int(value):
    """Convert an integer to its binary representation."""
    return bin(value)[2:]

def convert_to_different_numeric_base(value, base=10):
    """Convert a binary number to a different base."""
    bits = [int(x) for x in list(bin(value)[2:])]
    bits.reverse()
    return sum([base ** i * v for i, v in enumerate(bits)])

## BFS version, too slow   
# def get_part2_solution(parsed_data):
#     """Complete Part 2 solution here"""
#     total_min_presses = 0
#     for i, entry in enumerate(parsed_data):
#         buttons = entry['buttons']
#         joltages = entry['joltages']
#         # continue to treat offset as sort of bitmask for easier computation
#         # each place has more possible values than just 1 or 0, but we can still use the same logic
#         # to compute the minimum number of presses required
#         numeric_base = max(joltages)
#         target_joltage = sum([numeric_base ** i * v for i, v in enumerate(joltages)])
#         buttons = [convert_to_different_numeric_base(b, numeric_base) for b in buttons]
#         next_values = list(buttons)
#         min_presses = {b: 1 for b in buttons}
#         current_presses = 1
#         while target_joltage not in min_presses:
#             current_values = list(next_values)
#             next_values = []
#             for v in current_values:
#                 for b in buttons:
#                     next_v = v + b
#                     if next_v not in min_presses and next_v <= target_joltage:
#                         min_presses[next_v] = current_presses + 1
#                         next_values.append(next_v)
#             current_presses += 1

#         logger.debug(msg=f"entry {i} :: target {target_joltage} :: min_presses {min_presses[target_joltage]}")
#         total_min_presses += min_presses[target_joltage]
#     return total_min_presses

def dfs(remaining, min_presses, buttons):
    """Depth-first search to find the minimum number of presses required."""
    if remaining == 0:
        return 0
    if remaining < 0:
        return float('inf')
    if remaining in min_presses:
        return min_presses[remaining]

    min_count = float('inf')
    for b in buttons:
        if remaining % b == 0:
            count = dfs(remaining // b, min_presses, buttons) * remaining // b
        count = dfs(remaining - b, min_presses, buttons)
        if count != float('inf'):
            min_count = min(min_count, count + 1)
    min_presses[remaining] = min_count
    return min_count

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    total_min_presses = 0
    for i, entry in enumerate(parsed_data):
        buttons = entry['buttons']
        joltages = entry['joltages']
        # continue to treat offset as sort of bitmask for easier computation
        # each place has more possible values than just 1 or 0, but we can still use the same logic
        # to compute the minimum number of presses required
        numeric_base = max(joltages)
        target_joltage = sum([numeric_base ** i * v for i, v in enumerate(joltages)])
        buttons = [convert_to_different_numeric_base(b, numeric_base) for b in buttons]
        min_presses = {}
        min_presses[target_joltage] = dfs(target_joltage, min_presses, buttons)
        logger.debug(msg=f"entry {i} :: target {target_joltage} :: min_presses {min_presses[target_joltage]}")
        total_min_presses += min_presses[target_joltage]
    return total_min_presses

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
