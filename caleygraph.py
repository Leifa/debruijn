from pattern import Pattern
from relation import Relation


def compute_caley_graph(pattern):
    caley_graph = Pattern.empty_pattern()
    nodes = pattern.nodes

    diagonal = Relation.diagonal(pattern.get_number_of_nodes())
    green = pattern.green
    red = pattern.red

    caley_graph.add_node(diagonal.to_code(nodes))

    queue = [diagonal]
    while len(queue) > 0:
        current = queue.pop(0)

        # Add the green successor
        green_succ = current.compose(green)
        if green_succ.to_code(nodes) not in caley_graph.nodes:
            caley_graph.add_node(green_succ.to_code(nodes))
            queue.append(green_succ)
        caley_graph.add_green_edge(current.to_code(nodes), green_succ.to_code(nodes))

        # Add the red successor
        red_succ = current.compose(red)
        if red_succ.to_code(nodes) not in caley_graph.nodes:
            caley_graph.add_node(red_succ.to_code(nodes))
            queue.append(red_succ)
        caley_graph.add_red_edge(current.to_code(nodes), red_succ.to_code(nodes))

    return caley_graph

