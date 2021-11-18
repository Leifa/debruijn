from random import randint

class Pattern:

    def __init__(self):
        self.nodes = []
        self.red_succ = {}
        self.green_succ = {}
        self.red_pred = {}
        self.green_pred = {}

    @classmethod
    def from_edge_lists(cls, nodes, red, green):
        pattern = cls()
        for node in nodes:
            pattern.add_node(node)
        for (u, v) in red:
            pattern.add_red_edge(u, v)
        for (u, v) in green:
            pattern.add_green_edge(u, v)
        return pattern

    @classmethod
    def random_pattern(cls, number_of_nodes):
        pattern = cls()
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
        pattern = cls()
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

    def remove_useless_edges(self):
        # determine all nodes reachable from a selfloop
        red = set() # nodes reachable from a red selfloop via red edges
        green = set() # nodes reachable from a green selfloop via green edges
        for node in self.nodes:
            if node in self.red_succ[node]:
                red.add(node)
            if node in self.green_succ[node]:
                green.add(node)
        change = True
        while(change):
            change = False
            num_red = len(red)
            num_green = len(green)
            for node in red:
                red = red.union(self.red_succ[node])
            for node in green:
                green = green.union(self.green_succ[node])
            if len(red) > num_red or len(green) > num_green:
                change = True

        # if a node has an outgoing edge of color x, but is not reachable by a selfloop of color x, remove the edge
        for node in self.nodes:
            if node not in red:
                self.remove_all_red_successors(node)
            if node not in green:
                self.remove_all_green_successors(node)

    # removes all red successors of the given node
    def remove_all_red_successors(self, node):
        to_remove = set(self.red_succ[node])
        for node2 in to_remove:
            self.remove_red_edge(node, node2)

    # removes all green successors of the given node
    def remove_all_green_successors(self, node):
        to_remove = set(self.green_succ[node])
        for node2 in to_remove:
            self.remove_green_edge(node, node2)

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
        for node in self.red_succ:
            for node2 in self.red_succ[node]:
                new_red_edges.append((renaming[node], renaming[node2]))
        for node in self.green_succ:
            for node2 in self.green_succ[node]:
                new_green_edges.append((renaming[node], renaming[node2]))
        return self.from_edge_lists(new_nodes, new_red_edges, new_green_edges)

    def add_node(self, node):
        self.nodes.append(node)
        self.red_succ[node] = set()
        self.green_succ[node] = set()
        self.red_pred[node] = set()
        self.green_pred[node] = set()

    def add_red_edge(self, node1, node2):
        self.red_succ[node1].add(node2)
        self.red_pred[node2].add(node1)

    def add_green_edge(self, node1, node2):
        self.green_succ[node1].add(node2)
        self.green_pred[node2].add(node1)

    def remove_red_edge(self, node1, node2):
        self.red_succ[node1].remove(node2)
        self.red_pred[node2].remove(node1)

    def remove_green_edge(self, node1, node2):
        self.green_succ[node1].remove(node2)
        self.green_pred[node2].remove(node1)

    def has_red_edge(self, node1, node2):
        return node2 in self.red_succ[node1]

    def has_green_edge(self, node1, node2):
        return node2 in self.green_succ[node1]

    def get_number_of_nodes(self):
        return len(self.nodes)

    def get_number_of_red_edges(self):
        result = 0
        for node in self.red_succ:
            result += len(self.red_succ[node])
        return result

    def get_number_of_green_edges(self):
        result = 0
        for node in self.green_succ:
            result += len(self.green_succ[node])
        return result

    def remove_node(self, node):
        self.nodes.remove(node)
        del self.red_succ[node]
        del self.green_succ[node]
        del self.red_pred[node]
        del self.green_pred[node]
        for a in self.red_succ:
            if node in self.red_succ[a]:
                self.red_succ[a].remove(node)
        for a in self.green_succ:
            if node in self.green_succ[a]:
                self.green_succ[a].remove(node)
        for a in self.red_pred:
            if node in self.red_pred[a]:
                self.red_pred[a].remove(node)
        for a in self.green_pred:
            if node in self.green_pred[a]:
                self.green_pred[a].remove(node)

    def get_red_predecessors(self, node):
        return self.red_pred[node]

    def get_red_successors(self, node):
        return self.red_succ[node]

    def get_green_predecessors(self, node):
        return self.green_pred[node]

    def get_green_successors(self, node):
        return self.green_succ[node]

    def get_useless_nodes(self):

        useless_nodes = set()

        # nodes that have missing successors or predecessors
        for node in self.nodes:
            red_successor = len(self.red_succ[node]) > 0
            red_predecessor = len(self.red_pred[node]) > 0
            green_successor = len(self.green_succ[node]) > 0
            green_predecessor = len(self.green_pred[node]) > 0
            if not red_predecessor or not green_predecessor:
                useless_nodes.add(node)
                #print("Node " + str(node) + " does not have both colored predecessors and will be removed.")
            if not red_successor and not green_successor:
                useless_nodes.add(node)
                #print("Node " + str(node) + " does not have any successors and will be removed.")

        # nodes dominated by other nodes
        for i in range(len(self.nodes)):
            a = self.nodes[i]
            for j in range(i+1, len(self.nodes)):
                b = self.nodes[j]
                a_dominates_b = False
                b_dominates_a = False
                if self.red_pred[a].issubset(self.red_pred[b]) and \
                        self.red_succ[a].issubset(self.red_succ[b]) and \
                        self.green_pred[a].issubset(self.green_pred[b]) and \
                        self.green_succ[a].issubset(self.green_succ[b]):
                    b_dominates_a = True
                if self.red_pred[b].issubset(self.red_pred[a]) and self.red_succ[b].issubset(self.red_succ[a]) and \
                        self.green_pred[b].issubset(self.green_pred[a]) and self.green_succ[b].issubset(
                        self.green_succ[a]):
                    a_dominates_b = True
                if a_dominates_b:
                    useless_nodes.add(b)
                    #print("Node " + str(b) + " is dominated by " + str(a) + " and will be removed.")
                elif b_dominates_a:
                    useless_nodes.add(a)
                    #print("Node " + str(a) + " is dominated by " + str(b) + " and will be removed.")

        return useless_nodes

    def remove_useless_nodes(self):
        change_was_made = True
        while (change_was_made):
            to_remove = self.get_useless_nodes()
            change_was_made = False
            for node in to_remove:
                change_was_made = True
                self.remove_node(node)

    # returns True if node1 and node2 have a common red predecessor
    def common_red_pred(self, node1, node2):
        return len(self.red_pred[node1].intersection(self.red_pred[node2])) > 0

    # returns True if node1 and node2 have a common green predecessor
    def common_green_pred(self, node1, node2):
        return len(self.green_pred[node1].intersection(self.green_pred[node2])) > 0

    def L(self):
        prod = Pattern()
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

    def has_selfloop(self):
        for x in self.nodes:
            if self.has_red_edge(x, x) and self.has_green_edge(x, x):
                return True
        return False

    def has_green_selfloop(self):
        for x in self.nodes:
            if self.has_green_edge(x, x):
                return True
        return False

    def has_red_selfloop(self):
        for x in self.nodes:
            if self.has_red_edge(x, x):
                return True
        return False

    def log(self, nodes_and_edges=False):
        print("Number of Nodes: " + str(len(self.nodes)))
        if nodes_and_edges:
            print("Nodes: " + str(self.nodes))
            print("Green: " + str(self.green_succ))
            print("Red:   " + str(self.red_succ))
        print("Selfloop: " + str(self.has_selfloop()))