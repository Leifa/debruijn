import pysat.solvers

class SatSolver:

    def __init__(self):
        self.pattern1 = None
        self.pattern2 = None
        self.solver = pysat.solvers.MapleChrono()

    def make_clauses(self, pattern1, pattern2):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        n1 = pattern1.get_number_of_nodes()
        n2 = pattern2.get_number_of_nodes()

        # Every node from pattern1 has exactly one image in pattern2
        for i in range(n1):
            # Node i goes to at least one node from pattern2
            #print(list(range(n2*i+1, n2*(i+1)+1)))
            self.solver.add_clause(list(range(n2*i+1, n2*(i+1)+1)))
            # Node i does not go to two different nodes from pattern2
            for j in range(n2):
                for k in range(n2):
                    if j < k:
                        #print([-(n2*i+1+j), -(n2*i+1+k)])
                        self.solver.add_clause([-(n2*i+1+j), -(n2*i+1+k)])

        # For every green edge i1->i2 in pattern1: If i1 is mapped to j, then i2 has to be mapped to a successor of j
        for i1 in range(n1):
            for i2 in range(n1):
                if pattern1.has_green_edge(pattern1.nodes[i1], pattern1.nodes[i2]):
                    for j in range(n2):
                        antecendent = - (n2*i1+1+j)
                        green_succ_of_j = pattern2.get_green_successors(pattern2.nodes[j])
                        indices = pattern2.get_indices_of_nodes(green_succ_of_j)
                        literals = [n2*i2+1+j2 for j2 in indices]
                        literals.append(antecendent)
                        #print(literals)
                        self.solver.add_clause(literals)
        # For every red edge i1->i2 in pattern1: If i1 is mapped to j, then i2 has to be mapped to a successor of j
        for i1 in range(n1):
            for i2 in range(n1):
                if pattern1.has_red_edge(pattern1.nodes[i1], pattern1.nodes[i2]):
                    for j in range(n2):
                        antecendent = - (n2*i1+1+j)
                        red_succ_of_j = pattern2.get_red_successors(pattern2.nodes[j])
                        indices = pattern2.get_indices_of_nodes(red_succ_of_j)
                        literals = [n2*i2+1+j2 for j2 in indices]
                        literals.append(antecendent)
                        #print(literals)
                        self.solver.add_clause(literals)

    def has_homo(self):
        return self.solver.solve()

    def get_homo(self):
        assignment = self.solver.get_model()
        homo = {}
        n2 = self.pattern2.get_number_of_nodes()
        for i in assignment:
            if i > 0:
                i = i - 1
                node1 = i // n2
                node2 = i % n2
                homo[self.pattern1.nodes[node1]] = self.pattern2.nodes[node2]
        return homo


    def delete(self):
        self.solver.delete()
        del self.solver
