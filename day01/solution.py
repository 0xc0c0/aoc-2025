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
    rotation_cmds = [(line[0],int(line[1:])) for line in text_data.strip('\n ').split('\n')]
    return rotation_cmds

def get_part1_solution(rotation_cmds):
    """Complete Part 1 solution here"""
    placement = 50
    hits = 0
    for dir, dist in rotation_cmds:
        if dir == 'L':
            placement = (placement - dist) % 100
        else:
            placement = (placement + dist) % 100
        if placement == 0:
            hits += 1
    return hits

def get_part2_solution(rotation_cmds):
    """Complete Part 2 solution here"""
    rotations = []
    for d, dist in rotation_cmds:
        if d == 'L':
            rotations.append(-dist)
        else:
            rotations.append(dist)

    dial = 50
    total_hits = 0
    for r in rotations:
        #reduce r down to within 100
        total_hits += abs(r) // 100
        if r < 0:
            r = -(-r % 100)
        else:
            r = r % 100

        #get new dial position
        new_dial = (dial + r) % 100
        logger.debug(msg=f"{dial}, {r}, {new_dial}")
        # handle 0 crossing when negative
        # handle 0 crossing when positive
        zero_crossings = abs((dial + r) // 100)
        if dial == 0:
            zero_crossings -= 1
        if zero_crossings > 0:
            logger.debug(msg=f"  zero crossings: {zero_crossings}")
            total_hits += zero_crossings
        if new_dial == 0 and r < 0:
            logger.debug(msg="  landed on zero going left!")
            total_hits += 1
        
        dial = new_dial
    return total_hits

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
    rotation_cmds = parse_data(data)
    answer = get_part1_solution(rotation_cmds)
    print_answer(answer, part=1)
    answer = get_part2_solution(rotation_cmds)
    print_answer(answer, part=2)

if __name__ == '__main__':
    main()
