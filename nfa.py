class Nfa:

    def __init__(self, states, start, final, red, green):
        self.states = []
        self.start = start
        self.final = final
        self.red_succ = {}
        self.green_succ = {}
        self.red_pred = {}
        self.green_pred = {}
        for s in states:
            self.add_state(s)
        for (u, v) in red:
            self.add_red_edge(u, v)
        for (u, v) in green:
            self.add_green_edge(u, v)

    @classmethod
    def from_pattern_code(cls, number_of_nodes, code):
        nfa = Nfa([], None, None, [], [])
        for i in range(number_of_nodes):
            nfa.add_state(i)
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    nfa.add_green_edge(i, j)
                code = code // 2
        for i in range(number_of_nodes):
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    nfa.add_red_edge(i, j)
                code = code // 2
        return nfa

    def add_state(self, state):
        self.states.append(state)
        self.red_succ[state] = set()
        self.green_succ[state] = set()
        self.red_pred[state] = set()
        self.green_pred[state] = set()

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

    def get_red_predecessors(self, node):
        return self.red_pred[node]

    def get_red_successors(self, node):
        return self.red_succ[node]

    def get_green_predecessors(self, node):
        return self.green_pred[node]

    def get_green_successors(self, node):
        return self.green_succ[node]

    def power_nfa(self):
        queue = [{q} for q in self.states]
        nfa = Nfa([], None, None, [], [])
        while len(queue) > 0:
            state = frozenset(queue.pop(0))
            green_successor = set()
            red_successor = set()
            for s in state:
                green_successor = green_successor.union(self.get_green_successors(s))
                red_successor = red_successor.union(self.get_red_successors(s))
            green_successor = frozenset(green_successor)
            red_successor = frozenset(red_successor)
            if state not in nfa.states:
                nfa.add_state(state)
            if green_successor not in nfa.states:
                nfa.add_state(green_successor)
                if green_successor not in queue:
                    queue.append(green_successor)
            if red_successor not in nfa.states:
                nfa.add_state(red_successor)
                if red_successor not in queue:
                    queue.append(red_successor)
            nfa.add_green_edge(state, green_successor)
            nfa.add_red_edge(state, red_successor)

        return nfa

    def satisfies_path_condition(self):
        singletons = set([frozenset({q}) for q in self.states])
        all = frozenset(set(self.states))
        pow = self.power_nfa()
        reachable = pow.get_backwards_reachable_nodes(all)
        return singletons.issubset(reachable)

    # Returns the set of all nodes that are backwards reachable from the given node.
    def get_backwards_reachable_nodes(self, start):
        if start not in self.states:
            return {start}
        reachable = set()
        reachable.add(start)
        change = True
        while (change):
            change = False
            num_reachable = len(reachable)
            for node in reachable:
                reachable = reachable.union(self.red_pred[node]).union(self.green_pred[node])
            if len(reachable) > num_reachable:
                change = True
        return reachable


    def __repr__(self):
        return f"{self.states}\n{self.green_succ}\n{self.red_succ}"
