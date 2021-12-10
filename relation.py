class Relation:

    def __init__(self):
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

    # Returns the diagonal relation on the given number of nodes, also called the identity.
    @classmethod
    def diagonal(cls, number_of_nodes):
        relation = cls()
        for i in range(number_of_nodes):
            relation.add_node(i)
            relation.add_edge(i, i)
        return relation

    def add_node(self, node):
        self.succ[node] = set()
        self.pred[node] = set()

    def remove_node(self, node):
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

    def get_number_of_edges(self):
        result = 0
        for node in self.succ:
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
        for node in self.succ:
            if len(self.succ[node]) > 0:
                result.add(node)
        return result

    # Returns the set of all nodes that have at least one predecessor.
    def get_nodes_with_a_predecessor(self):
        result = set()
        for node in self.pred:
            if len(self.pred[node]) > 0:
                result.add(node)
        return result

    # Returns the set of all nodes that have a selfloop.
    def get_nodes_with_a_selfloop(self):
        selfloops = set()
        for node in self.succ:
            if node in self.succ[node]:
                selfloops.add(node)
        return selfloops

    def get_nodes_reachable_from_a_selfloop(self):
        result = set()
        for node in self.get_nodes_with_a_selfloop():
            result = result.union(self.get_reachable_nodes(node))
        return result

    # Returns True if there is a node that has a selfloop and such that all nodes are reachable from there.
    def has_selfloop_that_can_reach_all(self):
        all_nodes = set(self.succ.keys())
        for node in self.get_nodes_with_a_selfloop():
            if self.get_reachable_nodes(node) == all_nodes:
                return True
        return False

    # Returns True if there is a node that has a selfloop and such that all nodes are reachable from there.
    def get_selfloops_that_can_reach_all(self):
        selfloops_that_can_reach_all = set()
        all_nodes = set(self.succ.keys())
        for node in self.get_nodes_with_a_selfloop():
            if self.get_reachable_nodes(node) == all_nodes:
                selfloops_that_can_reach_all.add(node)
        return selfloops_that_can_reach_all

    # Removes all outgoing edges of the given node.
    def remove_all_successors(self, node):
        to_remove = set(self.succ[node])
        for node2 in to_remove:
            self.remove_edge(node, node2)

    # Given an ordered list of the nodes, this function computes the code of this relation.
    def to_code(self, nodes):
        number_of_nodes = len(nodes)
        code = 0
        current_bit = 1
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if self.has_edge(nodes[i], nodes[j]):
                    code += current_bit
                current_bit *= 2
        return number_of_nodes, code

    # Returns a new relation that is isomorphic to the old one, but names are according to the given renaming.
    # The renaming has to be a dictionary, the keys are the nodes, the values are the new names.
    def rename(self, renaming):
        new_relation = Relation()
        for node in self.succ:
            new_relation.add_node(renaming[node])
        for node in self.succ:
            for node2 in self.succ[node]:
                new_relation.add_edge(renaming[node], renaming[node2])
        return new_relation

    # returns True if node1 and node2 have a common predecessor
    def common_pred(self, node1, node2):
        return len(self.pred[node1].intersection(self.pred[node2])) > 0

    def has_selfloop(self):
        for node in self.succ:
            if self.has_edge(node, node):
                return True
        return False

    def union(self, other):
        union = Relation()
        for node in self.succ:
            union.add_node(node)
        for node in self.succ:
            for succ in self.succ[node]:
                union.add_edge(node, succ)
            for succ in other.succ[node]:
                union.add_edge(node, succ)
        return union

    def transitive_closure(self):
        tc = self
        change = True
        while change:
            change = False
            number_of_edges = tc.get_number_of_edges()
            tc = tc.union(tc.compose(self))
            if tc.get_number_of_edges() > number_of_edges:
                change = True
        return tc

    # Computes the composition of this relation with the given relation.
    def compose(self, rel2):
        composition = Relation()
        for node in self.succ:
            composition.add_node(node)
        for node in self.succ:
            for pred in self.pred[node]:
                for succ in rel2.succ[node]:
                    composition.add_edge(pred, succ)
        return composition

    # Returns whether the given node is a predecessor of every node.
    def sees_all(self, node):
        return self.succ[node] == set(self.succ.keys())

    def __eq__(self, other):
        if set(self.succ.keys()) != set(other.succ.keys()):
            return False
        for node in self.succ:
            if self.succ[node] != other.succ[node]:
                return False
        return True

    def __repr__(self):
        return str(self.succ)
