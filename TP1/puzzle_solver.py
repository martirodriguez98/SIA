import sys
from typing import Collection

from TP1.state import State


def main(config_file: str):
    states:Collection[State] = puzzle_solver()

def puzzle_solver()->Collection[State]:
    # TODO

if __name__ == "__main__":
    argv = sys.argv
    try:
        main(config_file)
    print('hola')
