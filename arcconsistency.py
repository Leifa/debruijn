from pattern import Pattern


class ArcConsistency:

    pattern1: Pattern
    pattern2: Pattern

    def __init__(self, pattern1, pattern2):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.candidates = {}

    def initialise_candidate_sets(self):
        full = set(self.pattern2.nodes)
        for node in self.pattern1.nodes:
            self.candidates[node] = set(full)

    def log_candidate_sets(self):
        print(self.candidates)

    def do_arc_consistency(self):
        change = True
        while change:
            total_number_of_candidates = sum(len(list) for list in self.candidates.values())
            for node1 in self.pattern1.nodes:
                for node2 in self.pattern1.get_green_successors(node1):
                    for candidate1 in self.candidates[node1]:
                        found_witness = False

                        # green successor
                        for candidate2 in self.candidates[node2]:
                            if self.pattern2.has_green_edge(candidate1, candidate2):
                                found_witness = True
                                break
                        if not found_witness:
                            print(f"Edge {node1}-{node2} first node candidate {candidate1} removed")
                            self.candidates[node1].remove(candidate1)
                            break
                    for candidate2 in self.candidates[node2]:
                        found_witness = False

                        # green successor
                        for candidate1 in self.candidates[node1]:
                            if self.pattern2.has_green_edge(candidate1, candidate2):
                                found_witness = True
                                break
                        if not found_witness:
                            print(f"Edge {node1}-{node2} second node candidate {candidate2} removed")
                            self.candidates[node2].remove(candidate2)
                            break

            for node1 in self.pattern1.nodes:
                for node2 in self.pattern1.get_red_successors(node1):
                    for candidate1 in self.candidates[node1]:
                        found_witness = False

                        # green successor
                        for candidate2 in self.candidates[node2]:
                            if self.pattern2.has_red_edge(candidate1, candidate2):
                                found_witness = True
                                break
                        if not found_witness:
                            print(f"Edge {node1}-{node2} first node candidate {candidate1} removed")
                            self.candidates[node1].remove(candidate1)
                            break
                    for candidate2 in self.candidates[node2]:
                        found_witness = False

                        # green successor
                        for candidate1 in self.candidates[node1]:
                            if self.pattern2.has_red_edge(candidate1, candidate2):
                                found_witness = True
                                break
                        if not found_witness:
                            print(f"Edge {node1}-{node2} second node candidate {candidate2} removed")
                            self.candidates[node2].remove(candidate2)
                            break

            for node1 in self.pattern1.nodes:
                if len(self.candidates[node1]) == 0:
                    return

            new_total_number_of_candidates = sum(len(list) for list in self.candidates.values())
            if new_total_number_of_candidates == total_number_of_candidates:
                change = False
