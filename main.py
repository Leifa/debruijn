import gc
from pattern import Pattern

diverging_dreier = Pattern.from_code(3, 44199)
converging = Pattern.from_code(4, 562287046)
erstes_schwieriges_vierer = Pattern.from_code(4, 224412099)
slow_square = Pattern.from_code(4, 3569496551)

def check_pattern(pattern):

    # some preprocessing
    if pattern.has_selfloop():
        return True
    pattern.remove_useless_edges()
    pattern.remove_useless_nodes()
    if len(pattern.nodes) == 0:
        return False
    if not pattern.has_green_selfloop() or not pattern.has_red_selfloop():
        return False

    # iterate L
    for i in range(7):
        if pattern.has_selfloop():
            return True
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
            return False
        #pattern.log()
    return -1

for code in range(2**22):
    pattern = Pattern.from_code(4, code)
    result = check_pattern(pattern)
    if code % 10000 == 0:
        print(code)
    if result == -1:
        print(str(code) + ": " + str(result))
