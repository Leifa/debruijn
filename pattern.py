from random import randint
from relation import Relation


class Pattern:

    def __init__(self, nodes, green, red):
        self.nodes = nodes
        self.green = green
        self.red = red

    @classmethod
    def empty_pattern(cls):
        return cls([], Relation(), Relation())

    @classmethod
    def from_edge_lists(cls, nodes, red_edges, green_edges):
        pattern = cls.empty_pattern()
        for node in nodes:
            pattern.add_node(node)
        for (u, v) in red_edges:
            pattern.red.add_edge(u, v)
        for (u, v) in green_edges:
            pattern.green.add_edge(u, v)
        return pattern

    @classmethod
    def random_pattern(cls, number_of_nodes):
        pattern = cls.empty_pattern()
        for i in range(number_of_nodes):
            pattern.add_node(i)
        for u in pattern.nodes:
            for v in pattern.nodes:
                if randint(0, 1):
                    pattern.add_green_edge(u, v)
                if randint(0, 1):
                    pattern.add_red_edge(u, v)
        return pattern

    @classmethod
    def from_code(cls, number_of_nodes, code):
        pattern = cls.empty_pattern()
        for i in range(number_of_nodes):
            pattern.add_node(i)
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    pattern.add_green_edge(i, j)
                code = code // 2
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    pattern.add_red_edge(i, j)
                code = code // 2
        return pattern

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
        self.red.add_node(node)
        self.green.add_node(node)

    def add_red_edge(self, node1, node2):
        self.red.add_edge(node1, node2)

    def add_green_edge(self, node1, node2):
        self.green.add_edge(node1, node2)

    def remove_red_edge(self, node1, node2):
        self.red.remove_edge(node1, node2)

    def remove_green_edge(self, node1, node2):
        self.green.remove_edge(node1, node2)

    def has_red_edge(self, node1, node2):
        return self.red.has_edge(node1, node2)

    def has_green_edge(self, node1, node2):
        return self.green.has_edge(node1, node2)

    def get_number_of_nodes(self):
        return len(self.nodes)

    def get_number_of_red_edges(self):
        return self.red.get_number_of_edges()

    def get_number_of_green_edges(self):
        return self.green.get_number_of_edges()

    def get_indices_of_nodes(self, set_of_nodes):
        indices = []
        for index in range(self.get_number_of_nodes()):
            if self.nodes[index] in set_of_nodes:
                indices.append(index)
        return indices

    def remove_node(self, node):
        self.nodes.remove(node)
        self.green.remove_node(node)
        self.red.remove_node(node)

    def get_red_predecessors(self, node):
        return self.red.get_predecessors(node)

    def get_red_successors(self, node):
        return self.red.get_successors(node)

    def get_green_predecessors(self, node):
        return self.green.get_predecessors(node)

    def get_green_successors(self, node):
        return self.green.get_successors(node)

    def remove_useless_edges(self):
        # determine all nodes reachable from a selfloop
        good_green = self.green.get_nodes_reachable_from_a_selfloop()
        good_red = self.red.get_nodes_reachable_from_a_selfloop()

        # if a node has an outgoing edge of color x, but is not reachable by a selfloop of color x, remove the edge
        for node in self.nodes:
            if node not in good_green:
                self.remove_all_green_successors(node)
            if node not in good_red:
                self.remove_all_red_successors(node)

    # Returns the set of all nodes that are reachable from the given node via a directed path of red edges.
    def get_reachable_nodes_via_red(self, start):
        return self.red.get_reachable_nodes(start)

    # Returns the set of all nodes that are reachable from the given node via a directed path of red edges.
    def get_reachable_nodes_via_green(self, start):
        return self.green.get_reachable_nodes(start)

    # Returns the set of all nodes that have a red successor.
    def get_nodes_with_a_red_successor(self):
        return self.red.get_nodes_with_a_successor()

    # Returns the set of all nodes that have a green successor.
    def get_nodes_with_a_green_successor(self):
        return self.green.get_nodes_with_a_successor()

    # Returns the set of all nodes that have a red selfloop.
    def get_nodes_with_a_red_selfloop(self):
        return self.red.get_nodes_with_a_selfloop()

    # Returns the set of all nodes that have a green selfloop.
    def get_nodes_with_a_green_selfloop(self):
        return self.green.get_nodes_with_a_selfloop()

    # Checks whether there is a node v with a red selfloop such that every node with a red successor is reachable
    # from v via a directed path of red edges. If this is not the case, then the pattern can be ignored,
    # because there is an equivalent subset of the pattern.
    def check_red_connected(self):
        return self.red.has_selfloop_that_can_reach_all()

    # Checks whether there is a node v with a green selfloop such that every node with a green successor is reachable
    # from v via a directed path of green edges. If this is not the case, then the pattern can be ignored,
    # because there is an equivalent subset of the pattern.
    def check_green_connected(self):
        return self.green.has_selfloop_that_can_reach_all()

    # Checks whether the code describes a pattern in normal form.
    # Normal form means, that there are at least as many green
    # edges as red edges, and that the nodes are ordered ascending by the number of green successors,
    # and, if two nodes have the same number of green successors, by the number of red successors.
    # If a pattern is not in normal form, then it can be ignored, because one can produce an equivalent
    # pattern by reordering nodes and exchanging red and green.
    @classmethod
    def check_code_normal_form(self, number_of_nodes, code):
        number_of_edges = bin(code).count("1")
        number_of_red_edges = bin(code >> (number_of_nodes*number_of_nodes)).count("1")
        number_of_green_edges = number_of_edges - number_of_red_edges
        if number_of_red_edges > number_of_green_edges:
            return False
        number_of_green_successors = []
        for i in range(number_of_nodes):
            number_of_green_successors.append(bin(code % (2**number_of_nodes)).count("1"))
            code //= (2**number_of_nodes)
        number_of_red_successors = []
        for i in range(number_of_nodes):
            number_of_red_successors.append(bin(code % (2**number_of_nodes)).count("1"))
            code //= (2**number_of_nodes)
        for i in range(number_of_nodes-1):
            if number_of_green_successors[i] < number_of_green_successors[i+1]:
                return False
            if number_of_green_successors[i] == number_of_green_successors[i+1] and number_of_red_successors[i] < number_of_red_successors[i+1]:
                return False
        return True

    # removes all red successors of the given node
    def remove_all_red_successors(self, node):
        self.red.remove_all_successors(node)

    # removes all green successors of the given node
    def remove_all_green_successors(self, node):
        self.green.remove_all_successors(node)

    # Returns whether there are nodes without successor, without green predecessor, without red predecessor,
    # or dominated by another node.
    def has_useless_nodes(self):
        # Is there a node with missing successors or predecessors?
        for node in self.nodes:
            red_successor = len(self.red.succ[node]) > 0
            red_predecessor = len(self.red.pred[node]) > 0
            green_successor = len(self.green.succ[node]) > 0
            green_predecessor = len(self.green.pred[node]) > 0
            if not red_predecessor or not green_predecessor:
                return True
            if not red_successor and not green_successor:
                return True

        # Is there a node dominated by other node?
        for a in self.nodes:
            for b in self.nodes:
                if a != b:
                    if self.red.pred[a].issubset(self.red.pred[b]) and \
                            self.red.succ[a].issubset(self.red.succ[b]) and \
                            self.green.pred[a].issubset(self.green.pred[b]) and \
                            self.green.succ[a].issubset(self.green.succ[b]):
                        return True
                    if self.red.pred[b].issubset(self.red.pred[a]) and self.red.succ[b].issubset(self.red.succ[a]) and \
                            self.green.pred[b].issubset(self.green.pred[a]) and self.green.succ[b].issubset(
                            self.green.succ[a]):
                        return True
        return False

    def to_code(self):
        number_of_nodes = len(self.nodes)
        code = 0
        current_bit = 1
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if self.has_green_edge(self.nodes[i], self.nodes[j]):
                    code += current_bit
                current_bit *= 2
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if self.has_red_edge(self.nodes[i], self.nodes[j]):
                    code += current_bit
                current_bit *= 2
        return number_of_nodes, code

    # Returns a new pattern that is isomorphic to the old one, but names of nodes are integers
    def normalize_names(self):
        number_of_nodes = len(self.nodes)
        new_nodes = list(range(number_of_nodes))
        new_red_edges = []
        new_green_edges = []
        renaming = {}
        for i in range(number_of_nodes):
            renaming[self.nodes[i]] = i
        new_red = self.red.rename(renaming)
        new_green = self.green.rename(renaming)
        return Pattern(new_nodes, new_green, new_red)

    def get_useless_nodes(self):

        useless_nodes = set()

        # nodes that have missing successors or predecessors
        for node in self.nodes:
            red_successor = len(self.red.succ[node]) > 0
            red_predecessor = len(self.red.pred[node]) > 0
            green_successor = len(self.green.succ[node]) > 0
            green_predecessor = len(self.green.pred[node]) > 0
            if not red_predecessor or not green_predecessor:
                useless_nodes.add(node)
            if not red_successor and not green_successor:
                useless_nodes.add(node)

        # nodes dominated by other nodes
        for i in range(len(self.nodes)):
            a = self.nodes[i]
            for j in range(i+1, len(self.nodes)):
                b = self.nodes[j]
                a_dominates_b = False
                b_dominates_a = False
                if self.red.pred[a].issubset(self.red.pred[b]) and \
                        self.red.succ[a].issubset(self.red.succ[b]) and \
                        self.green.pred[a].issubset(self.green.pred[b]) and \
                        self.green.succ[a].issubset(self.green.succ[b]):
                    b_dominates_a = True
                if self.red.pred[b].issubset(self.red.pred[a]) and self.red.succ[b].issubset(self.red.succ[a]) and \
                        self.green.pred[b].issubset(self.green.pred[a]) and self.green.succ[b].issubset(
                        self.green.succ[a]):
                    a_dominates_b = True
                if a_dominates_b:
                    useless_nodes.add(b)
                elif b_dominates_a:
                    useless_nodes.add(a)

        return useless_nodes

    def remove_useless_nodes(self):
        change_was_made = True
        while (change_was_made):
            to_remove = self.get_useless_nodes()
            change_was_made = False
            for node in to_remove:
                change_was_made = True
                self.remove_node(node)

    # returns True if node1 and node2 have a common green predecessor
    def common_green_pred(self, node1, node2):
        return self.green.common_pred(node1, node2)

    # returns True if node1 and node2 have a common red predecessor
    def common_red_pred(self, node1, node2):
        return self.red.common_pred(node1, node2)

    def lifting(self):
        prod = self.empty_pattern()
        for i in range(len(self.nodes)):
            for j in range(i, len(self.nodes)):
                # filter out nodes that will not have a green and a red predecessor in L(P)
                if self.common_green_pred(self.nodes[i], self.nodes[j]) and self.common_red_pred(self.nodes[i], self.nodes[j]):
                    prod.add_node((self.nodes[i], self.nodes[j]))
        for (u1, u2) in prod.nodes:
            for (v1, v2) in prod.nodes:
                if (self.has_red_edge(u1, v1) and self.has_red_edge(u1, v2)) or \
                        (self.has_red_edge(u2, v1) and self.has_red_edge(u2, v2)):
                    prod.add_red_edge((u1,u2), (v1,v2))
                if (self.has_green_edge(u1, v1) and self.has_green_edge(u1, v2)) or \
                        (self.has_green_edge(u2, v1) and self.has_green_edge(u2, v2)):
                    prod.add_green_edge((u1,u2), (v1,v2))
        return prod

    def has_green_selfloop(self):
        return self.green.has_selfloop()

    def has_red_selfloop(self):
        return self.red.has_selfloop()

    def has_double_selfloop(self):
        for x in self.nodes:
            if self.has_red_edge(x, x) and self.has_green_edge(x, x):
                return True
        return False

    # Takes a word (a list like [0, 1, 1]) and returns the set of all nodes that see themselves under this word.
    def get_relation_from_word(self, word):

        # Every node sees itself under the empty word
        if len(word) == 0:
            return set(self.nodes)

        relation = Relation.diagonal(len(self.nodes))

        for i in range(len(word)):
            if word[i] == 0:
                relation = relation.compose(self.green)
            elif word[i] == 1:
                relation = relation.compose(self.red)
            else:
                raise ValueError("Not an array of Ones and Zeros.")

        return relation

    def log(self, nodes_and_edges=False):
        print("Number of Nodes: " + str(len(self.nodes)))
        if nodes_and_edges:
            print("Nodes: " + str(self.nodes))
            print("Green: " + str(self.green.succ))
            print("Red:   " + str(self.red.succ))
        print("Selfloop: " + str(self.has_double_selfloop()))