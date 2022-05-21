import gc
from multiprocessing import Process
import time

from termcolor import colored

import codes
import constructiondeterministic
import homomorphism

import satsolver
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


def search_counterexample():
    number_of_nodes = 5
    count = 0
    while True:
        #time.sleep(0.001)
        count += 1
        code = codes.bias_random_code(5, 0.4)
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
    liftings = pattern.get_liftings()
    lifting_sizes = [str(l.get_number_of_nodes()) for l in liftings]
    print(f"Lifting sizes:         {', '.join(lifting_sizes)}")

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



def write_dict_to_file_sorted_by_keys(filename, dic):
    file = open(filename, "w")
    for key in sorted(dic):
        file.write(key + " : " + str(dic[key]) + "\n")
    file.close()




start_time = time.time()
log_pattern(4, 622074435)
end_time = time.time()
print(f"Finished in {end_time - start_time} seconds")
