from termcolor import colored

import caleygraph
import constructiondeterministic
import satsolver
from nfa import Nfa
from pattern import Pattern


def filter_patterns_using_first_path_condition_with_caleygraph(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        pattern = Pattern.from_code(int(number_of_nodes), int(code))
        caley_graph = caleygraph.CaleyGraph(pattern)
        if caley_graph.check_first_path_condition():
            count += 1
            output_file.write(f"{number_of_nodes},{code}")
        else:
            pattern.log(True)
        total += 1
        print(total)
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{count} of them satisfied the first path condition, {total - count} did not.")

def filter_patterns_using_second_path_condition_with_caleygraph(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        pattern = Pattern.from_code(int(number_of_nodes), int(code))
        caley_graph = caleygraph.CaleyGraph(pattern)
        if caley_graph.check_second_path_condition():
            count += 1
            output_file.write(f"{number_of_nodes},{code}")
        else:
            pattern.log(True)
        total += 1
        print(total)
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{count} of them satisfied the second path condition, {total - count} did not.")

def filter_patterns_using_construction_deterministic(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        pattern = Pattern.from_code(int(number_of_nodes), int(code))
        if not constructiondeterministic.is_construction_deterministic(pattern):
            count += 1
            output_file.write(f"{number_of_nodes},{code}")
        else:
            pattern.log(True)
        total += 1
        print(total)
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{total-count} of them are construction deterministic, {count} are not.")

def filter_patterns_using_first_path_condition(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        nfa = Nfa.from_pattern_code(int(number_of_nodes), int(code))
        all = nfa.states
        # print(nfa)
        nfa = nfa.power_nfa(full=True)
        nfa.clear_final_states()
        nfa.clear_start_states()
        for state in all:
            nfa.add_start_state(frozenset({state}))
        nfa.add_final_state(frozenset(all))
        if nfa.is_language_cofinite():
            count += 1
            output_file.write(f"{number_of_nodes},{code}")
        else:
            pattern = Pattern.from_code(int(number_of_nodes), int(code))
            # pattern.log(True)
        total += 1
        print(total)
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{count} of them satisfied the first path condition, {total - count} did not.")

def filter_patterns_using_sat_solver(input, solved, unsolved, number):
    input_file = open(input, "r")
    solved_file = open(solved, "a")
    unsolved_file = open(unsolved, "a")
    count = 0
    total = 0
    for line in input_file:
        if total == number:
            break
        number_of_nodes, code = line.split(",")
        pattern = Pattern.from_code(int(number_of_nodes), int(code))
        solved = False
        hom_until = 20
        n = hom_until
        while pattern.get_number_of_nodes() < 14:
            pattern = pattern.lifting().normalize_names()
            pattern.remove_useless_nodes()
            n = n - 1
        print(f"Check Homo from T_{n} to L^{hom_until - n}(P)")
        solver = satsolver.SatSolver()
        solver.make_hom_clauses(Pattern.T_n(n), pattern)
        if solver.solve():
            solved = True
        solver.delete()
        del solver
        if solved:
            print(colored(f'Homo at {hom_until}', "green"))
            solved_file.write(f"{number_of_nodes},{code}")
        else:
            count += 1
            print(colored(f'No homo until {hom_until}', "red"))
            unsolved_file.write(f"{number_of_nodes},{code}")
        total += 1
        print(total)
        del pattern
        gc.collect()
    input_file.close()
    solved_file.close()
    unsolved_file.close()
    print(f"Checked {total} patterns.")
    print(f"{total - count} have a hom at {hom_until}, {count} do not.")

def filter_patterns_using_third_path_condition(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        nfa = Nfa.from_pattern_code(int(number_of_nodes), int(code))
        if nfa.satisfies_path_condition():
            count += 1
            output_file.write(f"{number_of_nodes},{code}")
        else:
            pattern = Pattern.from_code(int(number_of_nodes), int(code))
            pattern.log(True)
        total += 1
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{count} of them satisfied the third path condition, {total - count} did not.")