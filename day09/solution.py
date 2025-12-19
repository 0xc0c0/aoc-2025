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
    parsed_data = [[int(x) for x in line.split(',')] for line in text_data.strip('\n ').split('\n')]
    return parsed_data

def get_part1_solution(parsed_data):
    """Complete Part 1 solution here"""
    highest_area = 0
    for i, entry1 in enumerate(parsed_data):
        for j, entry2 in enumerate(parsed_data, i+1):
            x1, y1 = entry1
            x2, y2 = entry2
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > highest_area:
                highest_area = area
    return highest_area

def get_sparse_entries(parsed_data):
    """Helper function to identify sparse entries"""
    orig_x_coords, orig_y_coords = zip(*parsed_data)
    x_coords = list(set(orig_x_coords))
    logger.debug(msg=f"Original unique X entries: {x_coords}")
    y_coords = list(set(orig_y_coords))
    logger.debug(msg=f"Original unique Y entries: {y_coords}")
    for i in range(len(x_coords)):
        x = x_coords[i]
        x_coords.append(x - 1)
        x_coords.append(x + 1)
    for i in range(len(y_coords)):
        y = y_coords[i]
        y_coords.append(y - 1)
        y_coords.append(y + 1)
    sparse_to_x = sorted(list(set(x_coords)))
    logger.debug(msg=f"Sparse X entries: {sparse_to_x}")
    sparse_to_y = sorted(list(set(y_coords)))
    logger.debug(msg=f"Sparse Y entries: {sparse_to_y}")
    x_to_sparse = {v: i for i, v in enumerate(sparse_to_x)}
    y_to_sparse = {v: i for i, v in enumerate(sparse_to_y)}

    return x_to_sparse, y_to_sparse, sparse_to_x, sparse_to_y

def check_all_points_filled(sparse_matrix, sx1, sy1, sx2, sy2):
    """Check if all points in the rectangle defined by (sx1, sy1) and (sx2, sy2) are filled"""
    for x in range(min(sx1, sx2), max(sx1, sx2) + 1):
        for y in range(min(sy1, sy2), max(sy1, sy2) + 1):
            if sparse_matrix[x][y] <= 0:
                return False
    return True

def get_part2_solution(parsed_data):
    """Complete Part 2 solution here"""
    # Build sparse mappings
    x_to_sparse, y_to_sparse, sparse_to_x, sparse_to_y = get_sparse_entries(parsed_data)

    # Initialize sparse matrix
    sparse_matrix = [[0 for _ in range(len(sparse_to_y))] for _ in range(len(sparse_to_x))]

    # Populate sparse matrix
    last_sp = None
    for x, y in parsed_data:
        sx = x_to_sparse[x]
        sy = y_to_sparse[y]
        sparse_matrix[sx][sy] = 1 # mark as corner (red)
        if last_sp is None:
            last_sp = (sx, sy)
        else:
            # Fill in between last_sp and current (sx, sy)
            lx, ly = last_sp
            if lx == sx:
                for y_fill in range(min(ly, sy), max(ly, sy) + 1):
                    if sparse_matrix[lx][y_fill] == 0:
                        sparse_matrix[lx][y_fill] = 2 # mark as edge (green)
            elif ly == sy:
                for x_fill in range(min(lx, sx), max(lx, sx) + 1):
                    if sparse_matrix[x_fill][ly] == 0:
                        sparse_matrix[x_fill][ly] = 2 # mark as edge (green)
            else:
                logger.error("Diagonal movement not supported")
            last_sp = (sx, sy)

    # Fill in from last point to first point to close the loop
    sx = x_to_sparse[parsed_data[0][0]]
    sy = y_to_sparse[parsed_data[0][1]]
    lx, ly = last_sp
    if lx == sx:
        for y_fill in range(min(ly, sy), max(ly, sy) + 1):
            if sparse_matrix[lx][y_fill] == 0:
                sparse_matrix[lx][y_fill] = 2 # mark as edge (green)
    elif ly == sy:
        for x_fill in range(min(lx, sx), max(lx, sx) + 1):
            if sparse_matrix[x_fill][ly] == 0:
                sparse_matrix[x_fill][ly] = 2 # mark as edge (green)
    else:
        logger.error("Diagonal movement not supported")

    points = set([(0,0)])
    while points:
        x, y = points.pop()
        # if point is unmarked, mark as outside and add neighbors
        if sparse_matrix[x][y] == 0:
            sparse_matrix[x][y] = -1 # mark as outside (blue)
            for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(sparse_to_x) and 0 <= ny < len(sparse_to_y):
                    if sparse_matrix[nx][ny] == 0:
                        points.add((nx, ny))

    for i, row in enumerate(sparse_matrix):
        for j, val in enumerate(row):
            if val == 0:
                sparse_matrix[i][j] = 3 # mark as inside (yellow)

    # Review all point combinations for valid areas in sparse matrix and track the highest area
    highest_area = 0
    for i, entry1 in enumerate(parsed_data):
        for _, entry2 in enumerate(parsed_data, i+1):
            x1, y1 = entry1
            x2, y2 = entry2
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            sx1, sx2 = x_to_sparse[x1], x_to_sparse[x2]
            sy1, sy2 = y_to_sparse[y1], y_to_sparse[y2]
            valid = check_all_points_filled(sparse_matrix, sx1, sy1, sx2, sy2)
            if valid and area > highest_area:
                highest_area = area
    return highest_area

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
