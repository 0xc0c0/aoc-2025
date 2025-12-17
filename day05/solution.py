#!/usr/bin/env python3

import copy
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
    ranges_text, ingredients_text = text_data.strip('\n ').split('\n\n')
    ranges = [[int(num) for num in line.split('-')] for line in ranges_text.split('\n')]
    ingredients = [int(x) for x in ingredients_text.strip('\n ').split('\n')]
    return ranges, ingredients

def get_part1_solution(ranges, ingredients):
    """Complete Part 1 solution here"""
    total_fresh = 0
    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                total_fresh += 1
                break
    return total_fresh

def merge_ranges(ranges):
    """Merge overlapping ranges into a list of non-overlapping ranges."""
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = []
    for current in sorted_ranges:
        if not merged or merged[-1][1] < current[0] - 1:
            merged.append(current)
        else:
            merged[-1][1] = max(merged[-1][1], current[1])
    return merged

def get_part2_solution(ranges):
    """Complete Part 2 solution here"""
    merged_ranges = merge_ranges(ranges)
    totals = [r[1] - r[0] + 1 for r in merged_ranges]
    return sum(totals)

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
    ranges, ingredients = parse_data(data)
    answer = get_part1_solution(ranges, ingredients)
    print_answer(answer, part=1)
    answer = get_part2_solution(ranges)
    print_answer(answer, part=2)

if __name__ == '__main__':
    main()
