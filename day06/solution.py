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
    lines = text_data.strip('\n ').split('\n')
    operators = lines[-1].split()
    number_rows = [[int(x) for x in line.strip().split()] for line in lines[:-1]]
    number_lists = list(zip(*number_rows))
    return number_lists, operators

def check_empty_column(num_lines, index):
    """Check if a given column index is empty across all lines."""
    for line in num_lines:
        if line[index] != ' ':
            return False
    return True

def parse_data2(text_data):
    """Alternative parsing function if needed for Part 2."""
    lines = text_data.strip('\n').split('\n')
    operator_line = lines[-1]
    num_lines = lines[:-1]
    number_lists = []
    operators = []
    nums = []
    for i, char in enumerate(operator_line):
        if char in '+*':
            operators.append(char)
        if not check_empty_column(num_lines, i):
            num = int(''.join([line[i] for line in num_lines if line[i] != ' ']))
            nums.append(num)
        if check_empty_column(num_lines, i) or i == len(operator_line) - 1:
            number_lists.append(nums)
            nums = []

    return number_lists, operators

def get_part1_solution(number_lists, operators):
    """Complete Part 1 solution here"""
    results = []
    for nums, op in zip(number_lists, operators):
        if op == '+':
            result = sum(nums)
            results.append(result)
        elif op == '*':
            result = 1
            for n in nums:
                result *= n
            results.append(result)
        else:
            logger.error(msg=f"Unknown operator: {op}")
            continue
        logger.debug(msg=f"Operation {op} on {nums} gives result {result}")
    return sum(results)

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
    answer = get_part1_solution(*parsed_data)
    print_answer(answer, part=1)
    parsed_data = parse_data2(data)
    answer = get_part1_solution(*parsed_data)
    print_answer(answer, part=2)

if __name__ == '__main__':
    main()
