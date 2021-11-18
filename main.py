import gc

from termcolor import colored

from pattern import Pattern

diverging_dreier = Pattern.from_code(3, 44199)
converging = Pattern.from_code(4, 562287046)
erstes_schwieriges_vierer = Pattern.from_code(4, 224412099)
slow_square = Pattern.from_code(4, 3569496551)
disconnected_red = Pattern.from_code(4, 2954840)
long_four = Pattern.from_code(4, 3937948)

def check_pattern(pattern):

    # some preprocessing
    if pattern.has_selfloop():
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
    for i in range(6):
        if pattern.has_selfloop():
            return 3
        num_nodes = pattern.get_number_of_nodes()
        num_red_edges = pattern.get_number_of_red_edges()
        num_green_edges = pattern.get_number_of_green_edges()
        pattern = pattern.L()
        pattern = pattern.normalize_names()
        gc.collect()  # call garbage collector to free memory
        pattern.remove_useless_nodes()
        if num_nodes == pattern.get_number_of_nodes() and \
                num_red_edges == pattern.get_number_of_red_edges() and \
                num_green_edges == pattern.get_number_of_green_edges():
            return 4
        pattern.log(True)
    return 5

long_four.log(True)
check_pattern(long_four)
quit()

results = [0, 0, 0, 0, 0, 0]

for code in range(3937900, 3938000):
    pattern = Pattern.from_code(4, code)
    #pattern.log(True)
    result = check_pattern(pattern)
    results[result] += 1
    if code % 1 == 0:
        print(code)
        print(results)

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
