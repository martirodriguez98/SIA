import sys
from typing import Collection

from TP1.puzzle_maker import create_puzzle
from TP1.state import State


# def main(config_file: str):
#     states:Collection[State] = puzzle_solver()

def main():
    puzzle_solver()

# def puzzle_solver()->Collection[State]:
#     # TODO
def puzzle_solver():
    create_puzzle()

if __name__ == "__main__":
    argv = sys.argv
    try:
        # main(config_file)
        main()

    except FileNotFoundError as e:
        print(f'Configuration file {e.filename} not found')

