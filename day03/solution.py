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
    parsed_data = [[int(x) for x in line] for line in parsed_data]
    return parsed_data

# def get_largest_joltage(bank):
#     """Helper function to get the largest joltage from the bank."""
#     first_digit = max(bank[:-1])
#     first_index = bank.index(first_digit)
#     second_digit = max(bank[first_index + 1:])
#     return int(str(first_digit) + str(second_digit))

def get_largest_joltage(bank, digits=2):
    """Helper function to get the largest joltage from the bank for part 2."""
    str_joltage = ''
    remaining_bank = bank[:]
    for i in range(digits):
        if i == digits - 1:
            digit = max(remaining_bank)
        else:
            digit = max(remaining_bank[:-(digits - i - 1)])
        digit_index = remaining_bank.index(digit)
        str_joltage += str(digit)
        # logger.debug(msg=f"Selected digit {digit} from bank {remaining_bank}")
        remaining_bank = remaining_bank[digit_index + 1:]
    return int(str_joltage)


def get_part1_solution(parsed_data):
    """Complete Part 1 solution here"""
    output_joltage = 0
    for bank in parsed_data:
        logger.debug(msg=f"Largest joltage for bank {bank} is {get_largest_joltage(bank)}")
        output_joltage += get_largest_joltage(bank)
    return output_joltage

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    output_joltage = 0
    for bank in parsed_data:
        logger.debug(msg=f"Largest joltage for bank {bank} is {get_largest_joltage(bank,12)}")
        output_joltage += get_largest_joltage(bank, digits=12)
    return output_joltage

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
