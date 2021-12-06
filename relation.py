class Relation:

    def __init__(self):
        self.nodes = []
        self.succ = {}
        self.pred = {}

    @classmethod
    def from_edge_list(cls, nodes, edges):
        relation = cls()
        for node in nodes:
            relation.add_node(node)
        for (u, v) in edges:
            relation.add_edge(u, v)
        return relation

    @classmethod
    def from_code(cls, number_of_nodes, code):
        relation = cls()
        for i in range(number_of_nodes):
            relation.add_node(i)
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    relation.add_edge(i, j)
                code = code // 2
        return relation

    def add_node(self, node):
        if node in self.nodes:
            return
        self.nodes.append(node)
        self.succ[node] = set()
        self.pred[node] = set()

    def remove_node(self, node):
        self.nodes.remove(node)
        del self.succ[node]
        del self.pred[node]
        for a in self.succ:
            if node in self.succ[a]:
                self.succ[a].remove(node)
        for a in self.pred:
            if node in self.pred[a]:
                self.pred[a].remove(node)

    def add_edge(self, node1, node2):
        self.succ[node1].add(node2)
        self.pred[node2].add(node1)

    def remove_edge(self, node1, node2):
        self.succ[node1].remove(node2)
        self.pred[node2].remove(node1)

    def has_edge(self, node1, node2):
        return node2 in self.succ[node1]

    def get_number_of_nodes(self):
        return len(self.nodes)

    def get_number_of_edges(self):
        result = 0
        for node in self.nodes:
            result += len(self.succ[node])
        return result

    def get_predecessors(self, node):
        return self.pred[node]

    def get_successors(self, node):
        return self.succ[node]

    # Returns the set of all nodes that are reachable from the given node via a directed path.
    def get_reachable_nodes(self, start):
        reachable = set()
        reachable.add(start)
        change = True
        while (change):
            change = False
            num_reachable = len(reachable)
            for node in reachable:
                reachable = reachable.union(self.succ[node]) # TODO: check if changing the set while iteration is ok
            if len(reachable) > num_reachable:
                change = True
        return reachable

    # Returns the set of all nodes that have at least one successor.
    def get_nodes_with_a_successor(self):
        result = set()
        for node in self.nodes:
            if len(self.succ[node]) > 0:
                result.add(node)
        return result

    # Returns the set of all nodes that have at least one predecessor.
    def get_nodes_with_a_predecessor(self):
        result = set()
        for node in self.nodes:
            if len(self.pred[node]) > 0:
                result.add(node)
        return result

    # Returns the set of all nodes that have a selfloop.
    def get_nodes_with_a_selfloop(self):
        selfloops = set()
        for node in self.nodes:
            if node in self.green_succ[node]:
                selfloops.add(node)
        return selfloops

    # Returns the set of roots. A node v is a root, if every node is reachable from v via a directed path.
    def get_roots(self):
        for node in self.nodes:
            reachable = self.get_reachable_nodes(node)
            if set(self.nodes).issubset(reachable):
                return True
        return False

    # Removes all outgoing edges of the given node.
    def remove_all_successors(self, node):
        to_remove = set(self.succ[node])
        for node2 in to_remove:
            self.remove_edge(node, node2)

    def to_code(self):
        number_of_nodes = len(self.nodes)
        code = 0
        current_bit = 1
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if self.has_edge(self.nodes[i], self.nodes[j]):
                    code += current_bit
                current_bit *= 2
        return number_of_nodes, code

    # Returns a new relation that is isomorphic to the old one, but names are according to the given renaming.
    # The renaming has to be a dictionary, the keys are the nodes, the values are the new names.
    def rename(self, renaming):
        new_relation = Relation()
        for node in self.nodes:
            new_relation.add_node(renaming[node])
        for node in self.succ:
            for node2 in self.succ[node]:
                new_relation.add_edge(renaming[node], renaming[node2])
        return new_relation

    # returns True if node1 and node2 have a common predecessor
    def common_pred(self, node1, node2):
        return len(self.pred[node1].intersection(self.pred[node2])) > 0

    def has_selfloop(self):
        for x in self.nodes:
            if self.has_edge(x, x):
                return True
        return False

    def log(self, nodes_and_edges=False):
        print("Number of Nodes: " + str(len(self.nodes)))
        if nodes_and_edges:
            print("Nodes: " + str(self.nodes))
            print("Edges: " + str(self.succ))
        print("Selfloop: " + str(self.has_selfloop()))