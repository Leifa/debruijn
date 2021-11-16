class Graph:

    def __init__(self):
        self.nodes = []
        self.red = []
        self.green = []

    def remove_node(self, node):
        self.nodes.remove(node)
        self.red = [edge for edge in self.red if node not in edge]
        self.green = [edge for edge in self.green if node not in edge]

    def get_red_predecessors(self, node):
        red_predecessors = set()
        for (x,y) in self.red:
            if y == node:
                red_predecessors.add(x)
        return red_predecessors

    def get_red_successors(self, node):
        red_successors = set()
        for (x,y) in self.red:
            if x == node:
                red_successors.add(y)
        return red_successors

    def get_green_predecessors(self, node):
        green_predecessors = set()
        for (x,y) in self.green:
            if y == node:
                green_predecessors.add(x)
        return green_predecessors

    def get_green_successors(self, node):
        green_successors = set()
        for (x,y) in self.green:
            if x == node:
                green_successors.add(y)
        return green_successors

    def get_useless_nodes(self):

        useless_nodes = set()

        # nodes that have missing successors or predecessors
        for node in self.nodes:
            red_successor = False
            red_predecessor = False
            green_successor = False
            green_predecessor = False
            for (x, y) in self.red:
                if node == x:
                    red_successor = True
                if node == y:
                    red_predecessor = True
            for (x, y) in self.green:
                if node == x:
                    green_successor = True
                if node == y:
                    green_predecessor = True
            if not red_predecessor or not green_predecessor:
                useless_nodes.add(node)
                print("Node " + str(node) + " does not have both colored predecessors and will be removed.")
            if not red_successor and not green_successor:
                useless_nodes.add(node)
                print("Node " + str(node) + " does not have any successors and will be removed.")

        # nodes dominated by other nodes
        for i in range(len(self.nodes)):
            a = self.nodes[i]
            red_preds_of_a = self.get_red_predecessors(a)
            green_preds_of_a = self.get_green_predecessors(a)
            red_succs_of_a = self.get_red_successors(a)
            green_succs_of_a = self.get_green_successors(a)
            for j in range(i+1, len(self.nodes)):
                b = self.nodes[j]
                red_preds_of_b = self.get_red_predecessors(b)
                green_preds_of_b = self.get_green_predecessors(b)
                red_succs_of_b = self.get_red_successors(b)
                green_succs_of_b = self.get_green_successors(b)
                a_dominates_b = False
                b_dominates_a = False
                if red_preds_of_a.issubset(red_preds_of_b) and red_succs_of_a.issubset(red_succs_of_b) and green_preds_of_a.issubset(green_preds_of_b) and green_succs_of_a.issubset(green_succs_of_b):
                    b_dominates_a = True
                if red_preds_of_b.issubset(red_preds_of_a) and red_succs_of_b.issubset(red_succs_of_a) and green_preds_of_b.issubset(green_preds_of_a) and green_succs_of_b.issubset(green_succs_of_a):
                    a_dominates_b = True
                if a_dominates_b:
                    useless_nodes.add(b)
                    print("Node " + str(b) + " is dominated by " + str(a) + " and will be removed.")
                elif b_dominates_a:
                    useless_nodes.add(a)
                    print("Node " + str(a) + " is dominated by " + str(b) + " and will be removed.")

        return useless_nodes

    def remove_useless_nodes(self):
        change_was_made = True
        while (change_was_made):
            to_remove = self.get_useless_nodes()
            change_was_made = False
            for node in to_remove:
                change_was_made = True
                self.remove_node(node)

    def L(self):
        prod = Graph()
        for i in range(len(self.nodes)):
            for j in range(i, len(self.nodes)):
                prod.nodes.append((self.nodes[i], self.nodes[j]))
        for (u1,u2) in prod.nodes:
            for (v1,v2) in prod.nodes:
                if ((u1,v1) in self.red and (u1,v2) in self.red) or ((u2,v1) in self.red and (u2,v2) in self.red):
                    prod.red.append(((u1,u2),(v1,v2)))
                if ((u1,v1) in self.green and (u1,v2) in self.green) or ((u2,v1) in self.green and (u2,v2) in self.green):
                    prod.green.append(((u1,u2),(v1,v2)))
        return prod

    def contains_selfloop(self):
        for x in self.nodes:
            if (x,x) in self.red and (x,x) in self.green:
                return True
        return False

    def log(self):
        print("Number of Nodes: " + str(len(self.nodes)))
        print("Nodes: " + str(self.nodes))
        print("Green: " + str(self.green))
        print("Red:   " + str(self.red))
        print("Selfloop: " + str(self.contains_selfloop()))

vierer = Graph()
vierer.nodes = ["a", "b", "c", "d"]
vierer.green = [("a", "a"), ("a", "b"), ("b", "c"), ("b", "d"), ("c", "a"), ("d", "c")]
vierer.red = [("b", "b"), ("b", "c"), ("c", "a"), ("c", "c"), ("c", "d")]

graph = vierer
for i in range(4):
    graph = graph.L()
    graph.remove_useless_nodes()
    graph.log()