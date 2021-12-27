import networkx as nx
import time
import argparse

from nqueens import solve_nqueens, print_queens_table, edge_populator

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nqueens')
parser.add_argument('-o', '--output')

args = parser.parse_args()
if args.nqueens is not None:
    N = int(args.nqueens)
else:
    N = 8

num_nodes = N**2

G = nx.empty_graph(num_nodes)

solutions = []

edge_populator(G, N)


start_time = time.time()
solve_nqueens(0, G, solutions, N)
final_time = time.time() - start_time

for solution_number, queens in enumerate(solutions):
    print_queens_table(queens, solution_number+1, N)

print(f"{N}-Queens has {len(solutions)} solutions found in {final_time:.5} seconds")

if args.output is not None:
    f = open(args.output, "a")
    f.write(f"{N},{len(solutions)},{final_time}\n")
    f.close()
