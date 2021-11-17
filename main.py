import gc
from termcolor import colored
from pattern import Pattern

diverging_dreier = Pattern.from_code(3, 44199)
converging = Pattern.from_code(4, 562287046)
erstes_schwieriges_vierer = Pattern.from_code(4, 224412099)
slow_square = Pattern.from_code(4, 3569496551)

print(colored('hello', 'green'))

graph = Pattern.random_pattern(3)
graph.log(nodes_and_edges=True)
if graph.has_green_selfloop() and graph.has_red_selfloop():
    for i in range(7):
        if graph.has_selfloop():
            break
        graph = graph.L()
        graph = graph.normalize_names()
        gc.collect() # call garbage collector to free memory
        graph.remove_useless_nodes()
        graph.log()
