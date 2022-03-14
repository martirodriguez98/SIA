import csv
import matplotlib.pyplot as plt
from typing import List, Optional

import numpy as np
import statistics as stats

from puzzle_maker import create_puzzle
from puzzle_solver import puzzle_solver
from state import State
from statistics import Statistics

from config_loader import StrategyParams

header = ['strategy', 'heuristic', 'result', 'cost', 'depth', 'expanded nodes', 'border nodes', 'limit',
          'processing_time']


def csv_results(file: str, data: List[List[str]]):
    with open(file, 'a') as f:
        writer = csv.writer(f)
        # write the header
        if not f.tell():
            writer.writerow(header)

        # write the data
        writer.writerows(data)

        f.close()

def generate_results(initial_state: State, strategy_name: str, strategy_params: Optional[StrategyParams] = None, heuristic=None, step=None):


    stats: Statistics = Statistics(strategy_name,strategy_params)

    data = []
    for i in range(20):
        puzzle_solver(initial_state, strategy_name, strategy_params, stats)

        data.append(
            [strategy_name, strategy_params['heuristic'] if strategy_params is not None and strategy_params['heuristic'] else "",
             stats.result, stats.cost, stats.depth, stats.expanded_nodes_count, stats.border_nodes_count,
             strategy_params['step'] if strategy_params is not None and strategy_params['step'] else "", stats.process_time])

    csv_results(f'{strategy_name}.csv', data)

def plot_uninformed():
    algorithms = ["BPA","BPP","BPPV"]
    results = {
        "BPA": {
            'time':[],
            'depth':[]
        },
        "BPP": {
            'time':[],
            'depth':[]
        },
        "BPPV": {
            'time':[],
            'depth':[]
        },
    }

    for a in algorithms:
        with open(f'{a}.csv',mode='r') as file:
            csv_file = csv.DictReader(csv_file)
            for row in csv_file:
                results[row['algorithm']]['time'].append(float(row['processing_time']))
                results[row['algorithm']]['depth'].append(int(row['depth']))

    barWidth = 0.25
    fig = plt.subplots(figsize=(12,8))

    # set height of bar
    IT = [12, 30, 1, 8, 22]
    ECE = [28, 6, 16, 5, 10]

    # Set position of bar on X axis
    br1 = np.arange(len(IT))
    br2 = [x + barWidth for x in br1]


    # Make the plot
    plt.bar(br1, IT, color ='r', width = barWidth,
        edgecolor ='grey', label ='TIME')
    plt.bar(br2, ECE, color ='g', width = barWidth,
        edgecolor ='grey', label ='COST')


    # Adding Xticks
    plt.xlabel('Branch', fontweight ='bold', fontsize = 15)
    plt.ylabel('Students passed', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(IT))],
            ['BPA', 'BPP', 'BPPV'])

    fig, time = plt.subplots()

    time.set_xlabel('ALGORITHM')
    time.set_ylabel('TIME (s)')

    time.bar(results.keys(),list(map(lambda a: fmean(a['time']),results.values())), color="red")

    cost = time.twinx()

    cost.set_ylabel('COST')

    cost.bar(results.keys(),list(map(lambda a: mean(a['cost']),results.values())),color="blue")

    plt.title('Uninformed searchs')
    plt.show()

if __name__ == "__main__":
    init_state = create_puzzle(100)
    generate_results(init_state, "BPA")
    generate_results(init_state,"BPP")
    generate_results(init_state,"BPPV",{"step":20,"heuristic":None})
    generate_results(init_state,"BPPV",{"step":50,"heuristic":None})
    generate_results(init_state,"BPPV",{"step":70,"heuristic":None})
    generate_results(init_state,"LOCAL_H",{"step":None,"heuristic":"manhattan_distance"})
    generate_results(init_state,"LOCAL_H",{"step":None,"heuristic":"hamming_distance"})
    generate_results(init_state,"LOCAL_H",{"step":None,"heuristic":"manhattan_hamming"})
    generate_results(init_state,"GLOBAL_H",{"step":None,"heuristic":"manhattan_distance"})
    generate_results(init_state,"GLOBAL_H",{"step":None,"heuristic":"hamming_distance"})
    generate_results(init_state,"GLOBAL_H",{"step":None,"heuristic":"manhattan_hamming"})
    generate_results(init_state,"A_STAR",{"step":None,"heuristic":"manhattan_distance"})
    generate_results(init_state,"A_STAR",{"step":None,"heuristic":"hamming_distance"})
    generate_results(init_state,"A_STAR",{"step":None,"heuristic":"manhattan_hamming"})

    plot_uninformed()