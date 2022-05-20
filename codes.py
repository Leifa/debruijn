# A pattern with n nodes is encoded as an integer using 2*n^2 bits as follows:
# The first n^2 bits (starting with LSB) encode the green edges, the other n^2 bits encode the red edges.
# The first n digits encode the incoming edges of node 0, the next n digits the incoming edges of node 1 and so on.
# Since we usually deal with patterns where every node has at least one incoming edge of each color,
# we do not need to encode the number of nodes. Instead, it can be deduced: A pattern with n nodes is encoded
# as a number that has at most 2*n^2 bits and at least 2*n^2-n+1 bits.

# Returns true iff the i-th bit of n equals 1.
def bit(n, i):
    return (n & (2**i)) > 0


# Converts the old code format into the new format. In the old format, bits were ordered such that the first
# n bits encoded the outgoing edges of node 0 instead of the incoming edges.
def old_code_to_new(number_of_nodes, code):
    result = 0
    for i in range(1, -1, -1):
        for j in range(number_of_nodes-1, -1, -1):
            for k in range(number_of_nodes-1, -1, -1):
                result *= 2
                if bit(code, number_of_nodes*number_of_nodes*i + number_of_nodes*k + j):
                    result += 1
    return result


# The code is interpreted as a pattern where every node has at least one predecessor of each color.
# In this case, we can uniquely determine the number of nodes of the pattern just from the length of the code.
def get_number_of_nodes(code):
    bits = 0
    while code > 0:
        code = code // 2
        bits = bits + 1
    nodes = 1
    while bits > 2*nodes*nodes:
        nodes = nodes + 1
    return nodes


# Does this pattern have a green edge from node i to node j?
def has_green_edge(number_of_nodes, code, i, j):
    return bit(code, number_of_nodes*j+i)


# Does this pattern have a green edge from node i to node j?
def has_red_edge(number_of_nodes, code, i, j):
    return bit(code, number_of_nodes*number_of_nodes + number_of_nodes*j+i)


# Returns a list of the green successors of the given node.
def get_green_successors(number_of_nodes, code, i):
    result = []
    for j in range(number_of_nodes):
        if has_green_edge(number_of_nodes, code, i, j):
            result.append(j)
    return result


# Returns a list of the green successors of the given node.
def get_red_successors(number_of_nodes, code, i):
    result = []
    for j in range(number_of_nodes):
        if has_red_edge(number_of_nodes, code, i, j):
            result.append(j)
    return result


# Returns a list of the green predecessors of the given node.
def get_green_predecessors(number_of_nodes, code, i):
    result = []
    for j in range(number_of_nodes):
        if has_green_edge(number_of_nodes, code, j, i):
            result.append(j)
    return result


# Returns a list of the red predecessors of the given node.
def get_red_predecessors(number_of_nodes, code, i):
    result = []
    for j in range(number_of_nodes):
        if has_red_edge(number_of_nodes, code, j, i):
            result.append(j)
    return result


# Returns a list of lists, the i-th list contains the successors of node i.
def get_green_successor_lists(number_of_nodes, code):
    result = []
    for i in range(number_of_nodes):
        result.append(get_green_successors(number_of_nodes, code, i))
    return result


# Returns a list of lists, the i-th list contains the successors of node i.
def get_red_successor_lists(number_of_nodes, code):
    result = []
    for i in range(number_of_nodes):
        result.append(get_red_successors(number_of_nodes, code, i))
    return result
