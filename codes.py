# A pattern with n nodes is encoded as an integer using 2*n^2 bits as follows:
# The first n^2 bits (starting with LSB) encode the green edges, the other n^2 bits encode the red edges.
# The first n digits encode the incoming edges of node 0, the next n digits the incoming edges of node 1 and so on.
# Since we usually deal with patterns where every node has at least one incoming edge of each color,
# we do not need to encode the number of nodes. Instead, it can be deduced: A pattern with n nodes is encoded
# as a number that has at most 2*n^2 bits and at least 2*n^2-n+1 bits.

# Returns true iff the i-th bit of n equals 1.
from random import random


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


# Returns a random code of a pattern of size n, where each bit has the given chance to be a 1.
# TODO: Return only patterns where every node has at least one incoming edge of each color.
def bias_random_code(n, chance):
    result = 0
    bits = 2*n*n
    for i in range(bits):
        result *= 2
        if random.random() < chance:
            result += 1
    return result


# Generates a list of all patterns that have hamming distance one from the given pattern.
# TODO: Let the hamming distance be an input parameter.
def generate_nearby_patterns(number_of_nodes, code):
    result = []
    for i in range(2*number_of_nodes**2):
        if bit(code, i):
            result.append(code - 2**i)
        else:
            result.append(code + 2**i)
    return result


def convert_file_from_old_to_new_format(input, output):
    input_file = open(input, "r")
    output_file = open(output, "a")
    for line in input_file:
        number_of_nodes, code = line.split(",")
        number_of_nodes = int(number_of_nodes)
        code = int(code)
        newcode = old_code_to_new(number_of_nodes, code)
        output_file.write(f"{newcode}\n")
    input_file.close()
    output_file.close()
