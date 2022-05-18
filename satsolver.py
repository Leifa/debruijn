import pysat.solvers
from pysat.formula import CNF

from pattern import Pattern


class SatSolver:

    def __init__(self):
        self.pattern1 = None
        self.pattern2 = None
        self.solver = pysat.solvers.MapleChrono()

    def make_hom_clauses(self, pattern1, pattern2):
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

    @classmethod
    def make_hom_clauses_cnf(self, pattern1, pattern2):
        cnf = CNF()

        self.pattern1 = pattern1
        self.pattern2 = pattern2
        n1 = pattern1.get_number_of_nodes()
        n2 = pattern2.get_number_of_nodes()

        # Every node from pattern1 has exactly one image in pattern2
        for i in range(n1):
            # Node i goes to at least one node from pattern2
            #print(list(range(n2*i+1, n2*(i+1)+1)))
            cnf.append(list(range(n2*i+1, n2*(i+1)+1)))
            # Node i does not go to two different nodes from pattern2
            for j in range(n2):
                for k in range(n2):
                    if j < k:
                        #print([-(n2*i+1+j), -(n2*i+1+k)])
                        cnf.append([-(n2*i+1+j), -(n2*i+1+k)])

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
                        cnf.append(literals)
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
                        cnf.append(literals)
        return cnf

    # Given n, a number of nodes and a code of a pattern, this returns a cnf that is satisfiable if and only if there
    # is a homomorphism from T_n to the pattern.

    @classmethod
    def code_to_cnf(self, n, number_of_nodes, code):
        cnf = CNF()
        green = []
        red = []
        for i in range(number_of_nodes):
            succ_of_i = []
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    succ_of_i.append(j)
                code = code // 2
            green.append(succ_of_i)
        for i in range(number_of_nodes):
            succ_of_i = []
            for j in range(number_of_nodes):
                if code % 2 == 1:
                    succ_of_i.append(j)
                code = code // 2
            red.append(succ_of_i)

        # Every node from pattern1 has exactly one image in pattern2
        for i in range(2**n):
            # Node i goes to at least one node from pattern2
            #print(list(range(n2*i+1, n2*(i+1)+1)))
            cnf.append(list(range(number_of_nodes*i+1, number_of_nodes*(i+1)+1)))
            # Node i does not go to two different nodes from pattern2
            for j in range(number_of_nodes):
                for k in range(j+1, number_of_nodes):
                    #print([-(n2*i+1+j), -(n2*i+1+k)])
                    cnf.append([-(number_of_nodes*i+1+j), -(number_of_nodes*i+1+k)])


        if n > 0:
            # For every green edge i->i2 in T_n: If i is mapped to j, then i2 has to be mapped to a green successor of j
            for j in range(number_of_nodes):
                for i in range(2**(n-1)):
                    i2 = 2*i
                    antecendent = - (number_of_nodes * i + 1 + j)
                    literals = [number_of_nodes * i2 + 1 + j2 for j2 in green[j]]
                    literals.append(antecendent)
                    cnf.append(literals)
                    i2 = 2*i+1
                    literals = [number_of_nodes * i2 + 1 + j2 for j2 in green[j]]
                    literals.append(antecendent)
                    cnf.append(literals)

            # For every red edge i->i2 in T_n: If i is mapped to j, then i2 has to be mapped to a red successor of j
            for j in range(number_of_nodes):
                for i in range(2**(n-1), 2**n):
                    i2 = i+i-2**n
                    antecendent = - (number_of_nodes * i + 1 + j)
                    literals = [number_of_nodes * i2 + 1 + j2 for j2 in red[j]]
                    literals.append(antecendent)
                    cnf.append(literals)
                    i2 = i+i-2**n+1
                    literals = [number_of_nodes * i2 + 1 + j2 for j2 in red[j]]
                    literals.append(antecendent)
                    cnf.append(literals)
        if n == 0:
            for j in range(number_of_nodes):
                i = 0
                i2 = 0
                antecendent = - (number_of_nodes * i + 1 + j)
                literals = [number_of_nodes * i2 + 1 + j2 for j2 in green[j]]
                literals.append(antecendent)
                cnf.append(literals)

            # For every red edge i->i2 in T_n: If i is mapped to j, then i2 has to be mapped to a red successor of j
            for j in range(number_of_nodes):
                i = 0
                i2 = 0
                antecendent = - (number_of_nodes * i + 1 + j)
                literals = [number_of_nodes * i2 + 1 + j2 for j2 in red[j]]
                literals.append(antecendent)
                cnf.append(literals)
        return cnf

    def make_hom_clauses_efficient(self, n, pattern):
        cnf = self.code_to_cnf(n, pattern.get_number_of_nodes(), pattern.to_code()[1])
        for clause in cnf:
            #print(clause)
            self.solver.add_clause(clause)

    def make_iso_clauses(self, pattern1, pattern2):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        n1 = pattern1.get_number_of_nodes()
        n2 = pattern2.get_number_of_nodes()

        self.make_hom_clauses(pattern1, pattern2)

        # Every node from pattern2 has exactly one preimage
        for j in range(n2):
            # Node j has at least one preimage in pattern1
            self.solver.add_clause(list(range(j+1, j+1+n1*n2, n2)))
            # Node j does not have two different preimages in pattern1
            for i in range(n1):
                for k in range(n1):
                    if i < k:
                        #print([-(n2*i+1+j), -(n2*i+1+k)])
                        self.solver.add_clause([-(n2*i+1+j), -(n2*k+1+j)])

        # For every green edge j1->j2 in pattern2: If j1 has preimage i, then j2 has preimage a green successor of i
        for j1 in range(n2):
            for j2 in range(n2):
                if pattern2.has_green_edge(pattern1.nodes[j1], pattern1.nodes[j2]):
                    for i in range(n1):
                        antecendent = - (n2*i+1+j1)
                        green_succ_of_i = pattern1.get_green_successors(pattern1.nodes[i])
                        indices = pattern1.get_indices_of_nodes(green_succ_of_i)
                        literals = [n2*i2+1+j2 for i2 in indices]
                        literals.append(antecendent)
                        #print(literals)
                        self.solver.add_clause(literals)

        # For every red edge j1->j2 in pattern2: If j1 has preimage i, then j2 has preimage a red successor of i
        for j1 in range(n2):
            for j2 in range(n2):
                if pattern2.has_red_edge(pattern1.nodes[j1], pattern1.nodes[j2]):
                    for i in range(n1):
                        antecendent = - (n2*i+1+j1)
                        red_succ_of_i = pattern1.get_red_successors(pattern1.nodes[i])
                        indices = pattern1.get_indices_of_nodes(red_succ_of_i)
                        literals = [n2*i2+1+j2 for i2 in indices]
                        literals.append(antecendent)
                        #print(literals)
                        self.solver.add_clause(literals)

    def make_relation_iso_clauses(self, rel1, rel2):
        n1 = rel1.get_number_of_nodes()
        n2 = rel2.get_number_of_nodes()
        nodes1 = list(rel1.succ.keys())
        nodes2 = list(rel2.succ.keys())

        # Every node from rel1 has exactly one image in rel2
        for i in range(n1):
            # Node i goes to at least one node from pattern2
            self.solver.add_clause(list(range(n2 * i + 1, n2 * (i + 1) + 1)))
            # Node i does not go to two different nodes from rel2
            for j in range(n2):
                for k in range(n2):
                    if j < k:
                        self.solver.add_clause([-(n2 * i + 1 + j), -(n2 * i + 1 + k)])

        # Every node from rel2 has exactly one preimage
        for j in range(n2):
            # Node j has at least one preimage in pattern1
            self.solver.add_clause(list(range(j+1, j+1+n1*n2, n2)))
            # Node j does not have two different preimages in pattern1
            for i in range(n1):
                for k in range(n1):
                    if i < k:
                        #print([-(n2*i+1+j), -(n2*i+1+k)])
                        self.solver.add_clause([-(n2*i+1+j), -(n2*k+1+j)])

        # For every edge i1->i2 in rel1: If i1 is mapped to j, then i2 has to be mapped to a successor of j
        for i1 in range(n1):
            for i2 in range(n1):
                if rel1.has_edge(nodes1[i1], nodes1[i2]):
                    for j in range(n2):
                        antecendent = - (n2 * i1 + 1 + j)
                        succ_of_j = rel2.get_successors(nodes2[j])
                        indices = rel2.get_indices_of_nodes(succ_of_j, nodes2)
                        literals = [n2 * i2 + 1 + j2 for j2 in indices]
                        literals.append(antecendent)
                        self.solver.add_clause(literals)

        # For every edge j1->j2 in rel2: If j1 has preimage i, then j2 has preimage a successor of i
        for j1 in range(n2):
            for j2 in range(n2):
                if rel2.has_edge(nodes2[j1], nodes2[j2]):
                    for i in range(n1):
                        antecendent = - (n2*i+1+j1)
                        succ_of_i = rel1.get_successors(nodes1[i])
                        indices = rel1.get_indices_of_nodes(succ_of_i, nodes1)
                        literals = [n2*i2+1+j2 for i2 in indices]
                        literals.append(antecendent)
                        self.solver.add_clause(literals)

    def solve(self):
        return self.solver.solve()

    def get_homo(self, n2):
        return self.solver.get_model()
        assignment = self.solver.get_model()
        homo = {}
        for i in assignment:
            if i > 0:
                i = i - 1
                node1 = i // n2
                node2 = i % n2
                homo[node1] = node2
        return homo


    def delete(self):
        self.solver.delete()
        del self.solver
