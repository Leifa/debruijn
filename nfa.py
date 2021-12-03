class Nfa:

    def __init__(self):
        self.states = set()
        self.start = set()
        self.final = set()
        self.red_succ = {}
        self.green_succ = {}
        self.red_pred = {}
        self.green_pred = {}

    @classmethod
    def from_pattern_code(cls, number_of_nodes, code):
        nfa = cls()
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
        self.states.add(state)
        self.red_succ[state] = set()
        self.green_succ[state] = set()
        self.red_pred[state] = set()
        self.green_pred[state] = set()

    def remove_state(self, state):
        if state in self.states:
            self.states.remove(state)
        if state in self.red_succ:
            del self.red_succ[state]
        if state in self.red_pred:
            del self.red_pred[state]
        if state in self.green_succ:
            del self.green_succ[state]
        if state in self.green_pred:
            del self.green_pred[state]
        for other in self.states:
            if state in self.red_succ[other]:
                self.red_succ[other].remove(state)
            if state in self.red_pred[other]:
                self.red_pred[other].remove(state)
            if state in self.green_succ[other]:
                self.green_succ[other].remove(state)
            if state in self.green_pred[other]:
                self.green_pred[other].remove(state)

    def add_start_state(self, state):
        if state not in self.start:
            self.start.add(state)

    def add_final_state(self, state):
        if state not in self.final:
            self.final.add(state)

    def clear_start_states(self):
        self.start = set()

    def clear_final_states(self):
        self.final = set()

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

    def is_deterministic(self):
        if len(self.start) != 1:
            return False
        for state in self.states:
            if len(self.red_succ[state]) != 1 or len(self.green_succ[state]) != 1:
                return False
        return True

    def power_nfa(self, full):
        if full:
            queue = [{state} for state in self.states]
        else:
            queue = [self.start]
        pow = Nfa()
        pow.start = {frozenset(self.start)}
        while len(queue) > 0:
            state = frozenset(queue.pop(0))
            green_successor = set()
            red_successor = set()
            for s in state:
                green_successor = green_successor.union(self.get_green_successors(s))
                red_successor = red_successor.union(self.get_red_successors(s))
            green_successor = frozenset(green_successor)
            red_successor = frozenset(red_successor)
            if state not in pow.states:
                pow.add_state(state)
            if green_successor not in pow.states:
                pow.add_state(green_successor)
                if green_successor not in queue:
                    queue.append(green_successor)
            if red_successor not in pow.states:
                pow.add_state(red_successor)
                if red_successor not in queue:
                    queue.append(red_successor)
            pow.add_green_edge(state, green_successor)
            pow.add_red_edge(state, red_successor)
        pow.final = {macrostate for macrostate in pow.states if len(macrostate.intersection(self.final)) > 0}

        return pow

    # restricts the nfa to the given set of states
    def restrict_to(self, states):
        to_remove = set()
        for state in self.states:
            if state not in states:
                to_remove.add(state)
        for state in to_remove:
            self.remove_state(state)

    def complement(self):
        if not self.is_deterministic():
            raise ValueError("This NFA is not deterministic, I cannot complement it.")
        self.final = self.states.difference(self.final)

    def contains_cycle(self):
        relation = set()
        for state1 in self.states:
            for state2 in self.red_succ[state1]:
                relation.add((state1, state2))
            for state2 in self.green_succ[state1]:
                relation.add((state1, state2))
        change = True
        while change:
            for state in self.states:
                if (state, state) in relation:
                    return True
            change = False
            l = len(relation)
            to_add = set()
            for state1, state2 in relation:
                for state3, state4 in relation:
                    if state2 == state3:
                        to_add.add((state1, state4))
            relation = relation.union(to_add)
            if len(relation) > l:
                change = True
        return False

    # throws all states away that are not reachable by a start state or the cannot reach a final state
    def minimize(self):
        reachable_from_start = self.get_forwards_reachable_nodes(self.start)
        reachable_from_final = self.get_backwards_reachable_nodes(self.final)
        intersection = reachable_from_start.intersection(reachable_from_final)
        self.restrict_to(intersection)

    def is_language_cofinite(self):
        nfa = self
        if not self.is_deterministic():
            nfa = self.power_nfa(False)
        nfa.complement()
        return nfa.is_language_finite()

    def is_language_finite(self):
        self.minimize()
        return not self.contains_cycle()

    def satisfies_path_condition(self):
        singletons = set([frozenset({q}) for q in self.states])
        all = frozenset(set(self.states))
        pow = self.power_nfa()
        reachable = pow.get_backwards_reachable_nodes({all})
        return singletons.issubset(reachable)

    # Returns the set of all nodes that are backwards reachable from the given set of nodes.
    def get_backwards_reachable_nodes(self, start):
        if not start.issubset(self.states):
            return start
        reachable = start
        change = True
        while (change):
            change = False
            num_reachable = len(reachable)
            for node in reachable:
                reachable = reachable.union(self.red_pred[node]).union(self.green_pred[node])
            if len(reachable) > num_reachable:
                change = True
        return reachable

    # Returns the set of all nodes that are forwards reachable from the given node.
    def get_forwards_reachable_nodes(self, start):
        if not start.issubset(self.states):
            return start
        reachable = start
        change = True
        while (change):
            change = False
            num_reachable = len(reachable)
            for node in reachable:
                reachable = reachable.union(self.red_succ[node]).union(self.green_succ[node])
            if len(reachable) > num_reachable:
                change = True
        return reachable

    def __repr__(self):
        return f"{self.states}\nStart: {self.start}\nFinal: {self.final}\n{self.green_succ}\n{self.red_succ}"
