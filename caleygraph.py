from pattern import Pattern
from relation import Relation

class CaleyGraph:

    def __init__(self, pattern):
        self.pattern = pattern
        self.caley_graph = self.compute_caley_graph(pattern)
        self.start = Relation.diagonal(pattern.get_number_of_nodes())

    def compute_caley_graph(self, pattern):
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

    def get_nodes_reachable_by_infinitely_many_words(self):
        forget_colors = self.caley_graph.red.union(self.caley_graph.green)
        transitive_closure = forget_colors.transitive_closure()
        return transitive_closure.get_nodes_reachable_from_a_selfloop()

    def get_nodes_reachable_by_finitely_many_words(self):
        return set(self.caley_graph.nodes).difference(self.get_nodes_reachable_by_infinitely_many_words())

    def check_first_path_condition(self):
        finite = self.get_nodes_reachable_by_finitely_many_words()
        diag = self.start.to_code(self.pattern.nodes)
        if diag in finite:
            finite.remove(diag)
        for number, code in finite:
            rel = Relation.from_code(number, code)
            selfloops = rel.get_nodes_with_a_selfloop()
            if selfloops == set():
                print(f"No selfloop for relation {rel}")
                return False
            found_candidate = False
            for candidate in selfloops:
                if rel.sees_all(candidate):
                    found_candidate = True
                    break
                multiple = rel
                for i in range(self.caley_graph.get_number_of_nodes()):
                    multiple = multiple.compose(rel)
                    if multiple.sees_all(candidate):
                        found_candidate = True
                        break
                if found_candidate:
                    break
            if not found_candidate:
                print(f"Not found a candidate for relation {rel}")
                return False
        return True

    def check_second_path_condition(self):
        infinite = self.get_nodes_reachable_by_infinitely_many_words()
        for number, code in infinite:
            rel = Relation.from_code(number, code)
            if not rel.has_node_that_sees_all():
                return False
        return True
