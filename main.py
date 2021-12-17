import gc
from multiprocessing import Process
import time

from termcolor import colored

#import constructiondeterministic

import satsolver
from nfa import Nfa
from pattern import Pattern
import caleygraph

diverging_dreier = Pattern.from_code(3, 44199)
converging = Pattern.from_code(4, 562287046)
erstes_schwieriges_vierer = Pattern.from_code(4, 224412099)
slow_square = Pattern.from_code(4, 3569496551)
disconnected_red = Pattern.from_code(4, 2954840)
long_four = Pattern.from_code(4, 3937948)

def check_pattern(number_of_nodes, code):

    #if not Pattern.check_code_normal_form(number_of_nodes, code):
    #    return 6
    pattern = Pattern.from_code(number_of_nodes, code)

    # some preprocessing
    if pattern.has_double_selfloop():
        return 1
    if not pattern.has_green_selfloop() or not pattern.has_red_selfloop():
        return 0
    if pattern.has_useless_nodes():
        return 2
    if not pattern.check_red_connected():
        return 2
    if not pattern.check_green_connected():
        return 2
    pattern.remove_useless_edges()
    pattern.remove_useless_nodes()
    if len(pattern.nodes) == 0:
        return 0

    # iterate L
    for i in range(9):
        if pattern.has_double_selfloop():
            return 3
        num_nodes = pattern.get_number_of_nodes()
        num_red_edges = pattern.get_number_of_red_edges()
        num_green_edges = pattern.get_number_of_green_edges()
        if num_nodes > 100:
            return 5
        pattern = pattern.lifting()
        pattern = pattern.normalize_names()
        gc.collect()  # call garbage collector to free memory
        pattern.remove_useless_nodes()
        if num_nodes == pattern.get_number_of_nodes() and \
                num_red_edges == pattern.get_number_of_red_edges() and \
                num_green_edges == pattern.get_number_of_green_edges():
            return 4
        #pattern.log(True)
        print(len(pattern.nodes))
    return 5


def check_pattern_range(start, finish, filename):
    results = [0, 0, 0, 0, 0, 0, 0]
    for code in range(start, finish):
        result = check_pattern(4, code)
        results[result] += 1
        if result == 5:
            f = open(filename, "a")
            f.write(f"4,{code}\n")
            f.close()
        # if code % 1000 == 0:
        #     print(results)

        # if result == 0:
        #     print(str(code) + ": " + colored("Trivial No Homo", "green"))
        # if result == 1:
        #     print(str(code) + ": " + colored("Trivial Homo", "green"))
        # if result == 2:
        #     print(str(code) + ": " + colored("Ignore", "yellow"))
        # if result == 3:
        #     print(str(code) + ": " + colored("Non Trivial Homo", "yellow"))
        # if result == 4:
        #     print(str(code) + ": " + colored("Non Trivial No Homo", "yellow"))
        # if result == 5:
        #     print(str(code) + ": " + colored("UNKNOWN", "red"))
        # if result == 6:
        #     print(str(code) + ": " + colored("No Normal Form", "yellow"))
    #print(results)

def check_pattern_range_multicore(start, finish, batch_size, cores, filename):

    # Calculate how many batches and initialize batch counter
    batches = (finish - start) // batch_size
    current_batch = 0
    processes = []

    # Start the processes
    while current_batch < cores:
        p = Process(target=check_pattern_range, args=(start+batch_size*current_batch, start+batch_size*(current_batch+1), f"{current_batch}.txt"))
        current_batch += 1
        p.start()
        processes.append(p)

    # Check every second whether a process has finished. If this is the case, and if there are more batches,
    # then start the process again with the next batch.
    while current_batch < batches:
        time.sleep(1)
        for i in range(len(processes)):
            if current_batch < batches and not processes[i].is_alive():
                p = Process(target=check_pattern_range, args=(start+batch_size*current_batch, start+batch_size*(current_batch+1), f"{current_batch}.txt"))
                current_batch += 1
                p.start()
                processes[i] = p
                print(colored(f"{current_batch / batches * 100}%", "yellow"))

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Write all results into one file.
    f = open(filename, "a")
    for i in range(batches):
        try:
            f2 = open(f"{i}.txt", "r")
            f.write(f2.read())
            f2.close()
        except OSError:
            pass
    f.close()

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
    print(f"{count} of them satisfied the third path condition, {total-count} did not.")

def filter_patterns_using_first_path_condition(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        nfa = Nfa.from_pattern_code(int(number_of_nodes), int(code))
        all = nfa.states
        #print(nfa)
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
            #pattern.log(True)
        total += 1
        print(total)
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{count} of them satisfied the first path condition, {total-count} did not.")

def check_patterns_from_file(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    count = 0
    total = 0
    for line in input_file:
        number_of_nodes, code = line.split(",")
        result = check_pattern(int(number_of_nodes), int(code))
        if result == 3:
            print(colored(f"Code {code} SOLVED!!! Homo", "green"))
        elif result == 4:
            print(colored(f"Code {code} SOLVED!!! No Homo", "green"))
        else:
            count += 1
            output_file.write(f"{number_of_nodes},{code}")
        total += 1
        print(f"Count: {total}")
    input_file.close()
    output_file.close()
    print(f"Checked {total} patterns.")
    print(f"{total-count} were solved now.")

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
    print(f"{count} of them satisfied the first path condition, {total-count} did not.")

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
    print(f"{count} of them satisfied the second path condition, {total-count} did not.")

# def filter_patterns_using_construction_deterministic(input, output):
#     input_file = open(input, "r")
#     output_file = open(output, "a")
#     count = 0
#     total = 0
#     for line in input_file:
#         number_of_nodes, code = line.split(",")
#         pattern = Pattern.from_code(int(number_of_nodes), int(code))
#         if not constructiondeterministic.is_construction_deterministic(pattern):
#             count += 1
#             output_file.write(f"{number_of_nodes},{code}")
#         else:
#             pattern.log(True)
#         total += 1
#         print(total)
#     input_file.close()
#     output_file.close()
#     print(f"Checked {total} patterns.")
#     print(f"{total-count} of them are construction deterministic, {count} are not.")

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
        hom_until = 18
        n = hom_until
        while pattern.get_number_of_nodes() < 14:
            pattern = pattern.lifting().normalize_names()
            pattern.remove_useless_nodes()
            n = n - 1
        print(f"Check Homo from T_{n} to L^{hom_until-n}(P)")
        solver = satsolver.SatSolver()
        solver.make_clauses(Pattern.T_n(n), pattern)
        if solver.has_homo():
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
    print(f"{total-count} have a hom at {hom_until}, {count} do not.")

start_time = time.time()

#filter_patterns_using_first_path_condition_with_caleygraph("unsolved.txt", "new2.txt")

filter_patterns_using_sat_solver("unsolved.txt", "homo_at_18.txt", "unsolved_new.txt", 1000)

#check_patterns_from_file("unsolved.txt", "new3.txt")

#check_pattern(4,57164443)

#print(check_pattern(4,23731294))

#check_pattern_range_multicore(2**31 + 2**29, 2**32, 2**20, 8, "bla.txt")

# f = open("unsolved2.txt", "a")
# for i in range(8):
#     for j in range(8):
#         try:
#             f2 = open(f"u{i}-{j}.txt", "r")
#             f.write(f2.read())
#             f2.close()
#         except OSError:
#             pass
# f.close()
#
# f = open("unsolved3.txt", "a")
# for i in range(8, 16):
#     for j in range(8):
#         try:
#             f2 = open(f"u{i}-{j}.txt", "r")
#             f.write(f2.read())
#             f2.close()
#         except OSError:
#             pass
# f.close()

end_time = time.time()
print(f"Finished in {end_time - start_time} seconds")
