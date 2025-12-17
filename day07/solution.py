#!/usr/bin/env python3

import logging
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
    parsed_data = [list(line) for line in text_data.strip('\n ').split('\n')]
    return parsed_data

def get_part1_solution(parsed_data):
    """Complete Part 1 solution here"""
    beam_cols = set()
    beam_cols.add(parsed_data[0].index('S'))
    splits = 0
    for _, row in enumerate(parsed_data[1:]):
        next_beam_cols = beam_cols.copy()
        for c in beam_cols:
            if row[c] == '^':
                splits += 1
                if c - 1 >= 0:
                    next_beam_cols.add(c - 1)
                if c + 1 < len(row):
                    next_beam_cols.add(c + 1)
                next_beam_cols.remove(c)
        beam_cols = next_beam_cols
    return splits

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    starter_index = parsed_data[0].index('S')
    beam_cols = {starter_index: 1}
    for _, row in enumerate(parsed_data[1:]):
        next_beam_cols = {}
        for c, n in beam_cols.items():
            if row[c] == '^':
                if c - 1 in next_beam_cols:
                    next_beam_cols[c - 1] += n
                else:
                    next_beam_cols[c - 1] = n
                if c + 1 in next_beam_cols:
                    next_beam_cols[c + 1] += n
                else:
                    next_beam_cols[c + 1] = n
            if row[c] == '.':
                if c in next_beam_cols:
                    next_beam_cols[c] += n
                else:
                    next_beam_cols[c] = n
        beam_cols = next_beam_cols
    timelines = sum(beam_cols.values())
    return timelines

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
