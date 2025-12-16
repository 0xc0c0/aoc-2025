import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def print_answer(answer, part=1):
    os.path.dirname.strip('day')

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def parse_data(text_data):
    rotation_cmds = [(line[0],int(line[1:])) for line in text_data.strip('\n ').split('\n')]
    return rotation_cmds

def get_part1_solution(rotation_cmds):
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

def main():
    data = get_file_data()
    rotation_cmds = parse_data(data)
    answer = get_part1_solution(rotation_cmds)
    
    print(__file__)
    print(answer)

if __name__ == '__main__':
    main()

