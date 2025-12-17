#!/usr/bin/env python3

import logging
import os
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    """Read the input file and return its contents as a string."""
    with open(fn, encoding='utf-8') as f:
        data = f.read()
    return data

def parse_data(text_data):
    """Parse the input data and return as data ready for processing."""
    text_entries = text_data.strip('\n ').split(',')
    parsed_data = []
    for text_entry in text_entries:
        logger.debug(msg=f"Entry: {text_entry}")
        lower, upper = text_entry.split('-')
        parsed_data.append([int(lower),int(upper)])
    return parsed_data

def get_range_invalid_ids(lower, upper, repetitions=2):
    """Get list of invalid IDs in the given range."""
    invalid_ids = []
    test_id = lower
    while test_id <= upper:
        str_id = str(test_id)
        if len(str_id) % repetitions != 0:
            #this cannot work in the repetition count, jump up to next digit length
            next_power_of_10 = 10 ** (len(str_id))
            test_id = next_power_of_10
            continue

        repeater = str_id[:len(str_id)//repetitions]
        
        if test_id < int(repeater * repetitions):
            #jump to the next opportunity to form a double
            test_id = int(repeater * repetitions)
            continue
        if str_id == repeater * repetitions and test_id not in invalid_ids:
            #this is a valid id
            invalid_ids.append(test_id)
        #jump to next potential invalid id
        test_id = int(str(int(repeater) + 1) * repetitions)
    return invalid_ids

def get_part1_solution(parsed_data):
    """Complete Part 1 solution here"""
    all_invalid_ids = []
    for lower, upper in parsed_data:
        invalid_ids = get_range_invalid_ids(lower, upper)
        all_invalid_ids.extend(invalid_ids)
    logger.debug(msg=f"All invalid IDs: {all_invalid_ids}")
    return sum(set(all_invalid_ids))

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    all_invalid_ids = []
    for lower, upper in parsed_data:
        for r in range(2, len(str(upper)) + 1):
            invalid_ids = get_range_invalid_ids(lower, upper, repetitions=r)
            all_invalid_ids.extend(invalid_ids)
    logger.debug(msg=f"All invalid IDs: {all_invalid_ids}")
    return sum(set(all_invalid_ids))

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
