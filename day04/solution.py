#!/usr/bin/env python3

import logging
import copy
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    """Read the input file and return its contents as a string."""
    with open(fn, encoding='utf-8') as f:
        data = f.read()
    return data

def parse_data(text_data):
    """Parse the input data and return as data ready for processing."""
    parsed_data = [[0 if x == '.' else 1 for x in line] for line in text_data.strip('\n ').split('\n')]
    return parsed_data

def count_neighbors(r, c, data):
    """Check the neighbors of a cell at (r, c) in the data grid."""
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    count = 0
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(data) and 0 <= nc < len(data[0]):
            count += data[nr][nc]
    return count

def get_part1_solution(parsed_data):
    """Complete Part 1 solution here"""
    accessible_rolls = 0
    for r, row in enumerate(parsed_data):
        for c, value in enumerate(row):
            if value == 1 and count_neighbors(r, c, parsed_data) < 4:
                accessible_rolls += 1
                # logger.debug(msg=f"Accessible roll at ({r}, {c})")
    return accessible_rolls

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    data = copy.deepcopy(parsed_data)
    initial_rolls = sum([sum(x) for x in data])
    while True:
        accessible_rolls = 0
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                if value == 1 and count_neighbors(r, c, data) < 4:
                    accessible_rolls += 1
                    data[r][c] = 0  # Mark as accessed

        if accessible_rolls == 0:
            break
    final_rolls = sum([sum(x) for x in data])
    return initial_rolls - final_rolls

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
