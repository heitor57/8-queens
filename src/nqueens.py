import string

from clique import bron_kerbosch


class Colors:
    RESET = '\033[0m'
    DARK = '\033[30m'
    RESET_FOREGROUND = '\033[39m'

    class Backgrounds:
        ORANGE = '\033[43m'
        WHITE = '\033[47m'


EMPTY = " "
QUEEN = Colors.DARK + u"\u265B" + Colors.RESET_FOREGROUND


def int2ordinal(num):
    num = str(num)
    if len(num) > 2:
        end_digits = int(num) % 100
    else:
        end_digits = int(num) % 10
    if end_digits == 1:
        return (num + "st")
    if end_digits == 2:
        return (num + "nd")
    if end_digits == 3:
        return (num + "rd")
    else:
        return (num + "th")


def str_queens_tupĺe(queens, N):
    result_string = ""
    TABLE_CHARS = string.ascii_letters[:N]
    for i, position in enumerate(queens):
        x, y = int(position/N), position % N
        result_string += f"{TABLE_CHARS[y]}{N-x}"
        if i < len(queens)-1:
            result_string += ","
    return result_string


def string_solution(solution_number, queens, N):
    return f"{int2ordinal(solution_number)} Solution → {str_queens_tupĺe(queens, N)}"


def print_queens_table(queens, solution_number, N):
    TABLE_CHARS = string.ascii_letters[:N]
    queens = list(queens)
    num_queens = len(queens)
    queens.sort()
    count = 0
    switch = 0
    if N % 2 == 0:
        sum_switch = 1
    else:
        sum_switch = 0

    # print("\u001b[0m")
    print("┌"+"─"*(3*N+1)+"┐", string_solution(solution_number, queens, N))
    for i in range(N**2):
        if i != 0 and i % N == 0:
            print(Colors.RESET)
            switch += sum_switch

        if i % N == 0:
            line_value_left = str(N-int(i/N))
            compesate_value = (len(str(N))-len(str(line_value_left)))
            print(" "+line_value_left+compesate_value*" ", end='')

        if (i+switch) % 2 == 0:
            print(Colors.Backgrounds.WHITE, end='')
        else:
            print(Colors.Backgrounds.ORANGE, end='')

        if count < num_queens and i == queens[count]:
            print(" "+QUEEN+" ", end='')
            count += 1
        else:
            print(" "+EMPTY+" ", end='')

    print(Colors.RESET)
    print("   "+"  ".join(TABLE_CHARS))

    print("└"+"─"*(3*N+1)+"┘")
    # print("\u001b[0m")


def solve_nqueens(column, G, solutions, N, queens=set()):
    if column == N:
        solutions.append(queens)
        return
    for current_row in range(N):
        vertex = column+current_row*N
        new_queens_set = queens.union(set([vertex]))
        sub_graph = G.subgraph(new_queens_set)
        # max_clique_size = nx.graph_clique_number(sub_graph)

        degrees = dict(sub_graph.degree)
        neighbors = dict(sub_graph.adj)
        for node in neighbors:
            neighbors[node] = set(neighbors[node])
        maximal_cliques = []
        bron_kerbosch(set(), new_queens_set.copy(), set(),
                      degrees, neighbors,
                      maximal_cliques)

        max_clique_size = 1
        for clique in maximal_cliques:
            max_clique_size = max(max_clique_size, len(clique))

        # if this check is true then it is a valid movement
        if max_clique_size == column+1:
            solve_nqueens(column+1, G, solutions, N, new_queens_set)


def edge_populator(G, N):
    num_nodes = G.number_of_nodes()
    # Add edges of the conditions to maintain
    for first_node in range(num_nodes):
        for second_node in range(num_nodes):
            if first_node != second_node and \
               (int(first_node/N) != int(second_node/N)) and \
               (int(first_node % N) != int(second_node % N)) and \
               ((int(first_node/N) + (first_node % N)) != (int(second_node/N) + (second_node % N))) and \
               ((int(first_node/N) - (first_node % N)) != (int(second_node/N) - (second_node % N))):
                G.add_edge(first_node, second_node)
