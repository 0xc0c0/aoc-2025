#!/usr/bin/env python3

import logging
import math
import os
import datetime

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    """Read the input file and return its contents as a string."""
    with open(fn, encoding='utf-8') as f:
        data = f.read()
    return data

def parse_data(text_data):
    """Parse the input data and return as data ready for processing."""
    parsed_data = [[int(x) for x in line.split(',')] for line in text_data.strip('\n ').split('\n')]
    return parsed_data

def craft_distance_lookup(parsed_data):
    """Create a distance lookup table for all points in parsed_data"""
    logger.debug(msg=f"Creating distance lookup for {len(parsed_data)} entries")
    logger.debug(msg=f"Starting at time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    distance_lookup = {}
    for i, entry in enumerate(parsed_data):
        for j, entry2 in enumerate(parsed_data):
            if i < j:
                distance_lookup[(i, j)] = (entry[0] - entry2[0])**2 + (entry[1] - entry2[1])**2 + (entry[2] - entry2[2])**2
    logger.debug(msg=f"Completed distance lookup at time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.debug(msg=f"Total distances calculated: {len(distance_lookup)}")
    return distance_lookup

def get_part1_solution(parsed_data, num_conn=10):
    """Complete Part 1 solution here"""
    dt = craft_distance_lookup(parsed_data)

    # index is which junction, value is which circuit it belongs to
    j_to_c = list(range(len(parsed_data)))

    # index is which circuit, value is list of junctions in that circuit
    # starts with each junction in its own circuit
    c = [[i] for i in range(len(parsed_data))]
    conn_made = 0
    while conn_made < num_conn:
        closest_pair = min(dt, key=dt.get)
        j1, j2 = closest_pair
        # get circuit indices
        c1 = j_to_c[j1]
        c2 = j_to_c[j2]

        # same circuit, skip
        if c1 == c2:
            logger.debug(msg=f"Pair {closest_pair} already in circuit {c1}, skipping")
        else:
            # new to merge each entry in circuit2 to circuit1
            while c[c2]:
                j = c[c2].pop()
                c[c1].append(j)
                j_to_c[j] = c1
            logger.debug(msg=f"Merged circuits {c2} into {c1}, new circuit:"
                        + f" {c[c1]}")
            logger.debug(msg=f"Circuit count: {len([c for c in c if c])}")
            logger.debug(msg=f"Current circuits: {c}")
            logger.debug(msg=f"Current junctions to circuits mapping: {j_to_c}")

        conn_made += 1
        logger.debug(msg=f"Connections made: {conn_made}/{num_conn}")
        del dt[closest_pair]
    sizes = [len(circuit) for circuit in c]
    max_3 = sorted(sizes, reverse=True)[:3]
    return math.prod(max_3)

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    dt = craft_distance_lookup(parsed_data)

    # index is which junction, value is which circuit it belongs to
    j_to_c = list(range(len(parsed_data)))

    # index is which circuit, value is list of junctions in that circuit
    # starts with each junction in its own circuit
    c = [[i] for i in range(len(parsed_data))]
    num_circuits = len([c for c in c if c])
    while num_circuits > 1:
        closest_pair = min(dt, key=dt.get)
        j1, j2 = closest_pair
        # get circuit indices
        c1 = j_to_c[j1]
        c2 = j_to_c[j2]

        # same circuit, skip
        if c1 == c2:
            logger.debug(msg=f"Pair {closest_pair} already in circuit {c1}, skipping")
        else:
            # new to merge each entry in circuit2 to circuit1
            while c[c2]:
                j = c[c2].pop()
                c[c1].append(j)
                j_to_c[j] = c1
            num_circuits -= 1
            logger.debug(msg=f"Merged circuits {c2} into {c1}, new circuit:"
                        + f" {c[c1]}")
            logger.debug(msg=f"Circuit count: {num_circuits}")
            # logger.debug(msg=f"Current circuits: {c}")
            # logger.debug(msg=f"Current junctions to circuits mapping: {j_to_c}")
        if num_circuits == 1:
            return parsed_data[j1][0] * parsed_data[j2][0]
        del dt[closest_pair]

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
    answer = get_part1_solution(parsed_data, num_conn=1000)
    print_answer(answer, part=1)
    answer = get_part2_solution(parsed_data)
    print_answer(answer, part=2)

if __name__ == '__main__':
    main()
