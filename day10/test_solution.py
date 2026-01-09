"""Python test file for unit testing in support of AoC solves"""
import os
import pytest
from .solution import parse_data, get_file_data, get_part1_solution, get_part2_solution


@pytest.fixture(name="test_data")
def get_test_data_1():
    """Provides test data using text.txt for return of file to consume

    Returns:
        str: data blob of text from file
    """
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.txt")
    return get_file_data(test_file)


@pytest.fixture(name="test_data2")
def get_test_data_2():
    """Provides test data using text2.txt for return of file to consume

    Returns:
        str: data blob of text from file
    """
    # dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test2.txt")
    return get_file_data(test_file)


def test_parse_input(test_data):
    """Test all parsing functions associated with Part 1

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    assert len(data) == 3
    assert data[0]['objective'] == 6
    assert data[0]['buttons'][0] == 8
    assert data[0]['buttons'][1] == 10
    assert len(data[0]['joltages']) == 4


def test_all(test_data):
    """Test all functions associated with Parts 1 and 2

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    assert get_part1_solution(data) == 7
    assert get_part2_solution(data) == 33
