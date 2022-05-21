import gc
import math
import random
from multiprocessing import Process
import time

from termcolor import colored

import caleygraph
import codes
import constructiondeterministic
import homomorphism

import satsolver
from nfa import Nfa
from pattern import Pattern
from caleygraph import CaleyGraph
from relation import Relation


def check_pattern(number_of_nodes, code):
    # if not Pattern.check_code_normal_form(number_of_nodes, code):
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
        # pattern.log(True)
        print(len(pattern.nodes))
    return 5

# Searches a homomorphism from a Tn into the pattern. The depth is the maximum n that is checked.
def search_homo(pattern, depth):
    if pattern.has_double_selfloop():
        return 0

    liftings = [pattern]
    last = pattern
    for i in range(depth):
        if last.get_number_of_nodes() > 30:
            break
        lifting = last.lifting()
        if lifting.has_double_selfloop():
            return i+1
        lifting.normalize_names()
        lifting.remove_useless_nodes()
        last = lifting
        liftings.append(last)

    best = 0
    for i in range(len(liftings) - 1):
        if liftings[i + 1].get_number_of_nodes() / liftings[i].get_number_of_nodes() < 2:
            best = i

    for n in range(len(liftings), depth + 1):
        solver = satsolver.SatSolver()
        solver.make_hom_clauses_efficient(n - best, liftings[best])
        if solver.solve():
            return n
        solver.delete()
        del solver
    return -1

def bias_random_code(n, chance):
    result = 0
    bits = 2*n*n
    for i in range(bits):
        result *= 2
        if random.random() < chance:
            result += 1
    return result


def search_counterexample():
    number_of_nodes = 5
    count = 0
    while True:
        #time.sleep(0.001)
        count += 1
        #code = random.randint(0, 2**50)
        code = bias_random_code(5, 0.4)
        print(f"{count} - {number_of_nodes}:{code}")
        pattern = Pattern.from_code(number_of_nodes, code)
        if constructiondeterministic.is_construction_deterministic(pattern):
            print("  no homo")
            continue
        cg = CaleyGraph(pattern)
        if not cg.check_first_path_condition() or not cg.check_second_path_condition() or not cg.check_third_path_condition():
            print("  no homo")
            continue
        homo_at = search_homo(pattern, 21)
        if homo_at == -1:
            log_pattern(number_of_nodes, code)
            break
        else:
            print(f"  homo at {homo_at}")


def log_pattern(number_of_nodes, code):
    YES = colored("YES", "green")
    NO = colored("NO", "red")
    pattern = Pattern.from_code(number_of_nodes, code)
    normal_form = Pattern.check_code_normal_form(number_of_nodes, code)
    print(f"==========================")
    pattern.log(True)
    print(f"Normal form:           {YES if normal_form else NO}")
    const_nondet = not constructiondeterministic.is_construction_deterministic(pattern)
    print(f"Construction nondet.:  {YES if const_nondet else NO}")
    print(f"Caleygraph size:       ", end="", flush=True)
    cg = CaleyGraph(pattern)
    print(f"{cg.caley_graph.get_number_of_nodes()}")
    first_pc = cg.check_first_path_condition()
    second_pc = cg.check_second_path_condition()
    third_pc = cg.check_third_path_condition()

    homo_at = -1
    solved = False
    if not const_nondet or not first_pc or not second_pc or not third_pc:
        solved = True
    print(f"First path condition:  {YES if first_pc else NO}")
    print(f"Second path condition: {YES if second_pc else NO}")
    print(f"Third path condition:  {YES if third_pc else NO}")
    if solved:
        print(colored("No surjective homomorphism", "red"))

    pattern.remove_useless_nodes()
    pattern.remove_useless_edges()
    liftings = [pattern]
    last = pattern
    print("Lifting sizes:         ", end="", flush=True)
    for i in range(10):
        if last.get_number_of_nodes() > 30:
            print(f"{last.get_number_of_nodes()}")
            break
        else:
            if i < 9:
                print(f"{last.get_number_of_nodes()}, ", end="", flush=True)
            else:
                print(f"{last.get_number_of_nodes()}, ")
        lifting = last.lifting()
        lifting.normalize_names()
        lifting.remove_useless_nodes()
        last = lifting
        liftings.append(last)

    if solved:
        return

    best = 0
    for i in range(len(liftings) - 1):
        if liftings[i + 1].get_number_of_nodes() / liftings[i].get_number_of_nodes() < 1.41421:
            best = i+1
    print(f"Best No. of Liftings:  {best}")
    for i in range(best+1):
        if liftings[i].has_double_selfloop():
            homo_at = i
            solved = True
            print(colored(f"Homomorphism at:       {homo_at}", "green"))
            return

    if not solved:
        print(f"No hom until:          {best-1}", end="", flush=True)

    for n in range(best, 23):
        solver = satsolver.SatSolver()
        solver.make_hom_clauses_efficient(n-best, liftings[best])
        if solver.solve():
            solved = True
            homo_at = n
            print(colored(f"\nHomomorphism at:       {homo_at}", "green"))
            hom = solver.get_homo(liftings[best].get_number_of_nodes())
            string_hom = homomorphism.convert_keys_of_hom_to_binary_strings(hom)
            compressed_hom = homomorphism.compress_homomorphism(string_hom)
            write_dict_to_file_sorted_by_keys("hom.txt", compressed_hom)
        else:
            print(f", {n}", end="", flush=True)
        solver.delete()
        del solver
        if solved:
            break
    print("")


def generate_nearby_patterns(number_of_nodes, code):
    result = []
    for i in range(2*number_of_nodes**2):
        if bit(code, i):
            result.append(code - 2**i)
        else:
            result.append(code + 2**i)
    return result


def bit(n, i):
    return (n // (2**i)) % 2


def find_good_relations():
    out = open("5er-relations.txt", "a")
    for code in range(2**25):
        if code % 10000 == 0:
            print(code)
        rel = Relation.from_code(5, code)
        if rel.has_selfloop_that_can_reach_all():
            out.write(f"{code}")
    out.close()


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
    # print(results)


def check_pattern_range_multicore(start, finish, batch_size, cores, filename):
    # Calculate how many batches and initialize batch counter
    batches = (finish - start) // batch_size
    current_batch = 0
    processes = []

    # Start the processes
    while current_batch < cores:
        p = Process(target=check_pattern_range, args=(
        start + batch_size * current_batch, start + batch_size * (current_batch + 1), f"{current_batch}.txt"))
        current_batch += 1
        p.start()
        processes.append(p)

    # Check every second whether a process has finished. If this is the case, and if there are more batches,
    # then start the process again with the next batch.
    while current_batch < batches:
        time.sleep(1)
        for i in range(len(processes)):
            if current_batch < batches and not processes[i].is_alive():
                p = Process(target=check_pattern_range, args=(
                start + batch_size * current_batch, start + batch_size * (current_batch + 1), f"{current_batch}.txt"))
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
    print(f"{count} of them satisfied the third path condition, {total - count} did not.")


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


def write_dict_to_file_sorted_by_keys(filename, dic):
    file = open(filename, "w")
    for key in sorted(dic):
        file.write(key + " : " + str(dic[key]) + "\n")
    file.close()


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
    print(f"{total - count} were solved now.")


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


def convert_file_from_old_to_new_format(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    for line in input_file:
        number_of_nodes, code = line.split(",")
        number_of_nodes = int(number_of_nodes)
        code = int(code)
        newcode = codes.old_code_to_new(number_of_nodes, code)
        output_file.write(f"{newcode}\n")
    input_file.close()
    output_file.close()


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

# Is the i-th bit of n a one?

def bit(n, i):
    return (n & (2**i)) > 0


start_time = time.time()

#convert_file_from_old_to_new_format(f"patternlists/5/homo_at_21.txt", f"patternlists/5/homo_at_21_new.txt")

#find_good_relations()

#search_counterexample()


# pat = generate_nearby_patterns(5, 846900323733667)
# for p in pat:
#     log_pattern(5, p)

#log_pattern(5, 846900323733667)
#log_pattern(5, 758207799374956) #hom at 20
log_pattern(4, 1108858424)

#log_pattern(4,2458141589) #hom at 20

#search_counterexample()

#log_pattern(5, 618273496900739+ 2**40)

# filter_patterns_using_first_path_condition_with_caleygraph("unsolved.txt", "new2.txt")

# filter_patterns_using_sat_solver("unsolved.txt", "homo_at_20.txt", "unsolved_new.txt", 1000)

# check_patterns_from_file("unsolved.txt", "new3.txt")

# check_pattern(4,57164443)

# print(check_pattern(4,23731294))

# check_pattern_range_multicore(2**31 + 2**29, 2**32, 2**20, 8, "bla.txt")

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
