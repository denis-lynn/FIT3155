# Denis Lynn
# 30580390
# This is currently non-functional but hopefully the comments give some insight into how I planned for it to
import sys


class GlobalEnd:
    # Storing Global end as an object in memory so all leaves can point to it
    def __init__(self, end_index=0):
        self.end = end_index

    def increment_end(self):
        self.end += 1


class Edge:
    # Edges can be leaf or edge_between_two_nodes and this depends on whether it has children or not
    def __init__(self, start_index, char, branch_off_node):
        self.start_index = start_index
        self.end_index = None
        self.character = char
        self.parent = branch_off_node
        self.child = None

    def is_leaf(self):
        # Checks if there are children
        edge_type = True
        if self.child:
            edge_type = False
        return edge_type

    def __len__(self):
        # Finds length depending on whether it is a leaf or an edge between nodes
        # Used for skip counting
        if type(self.end_index) is int:
            length = self.end_index - self.start_index + 1
        else:
            length = self.end_index.end - self.start_index + 1
        return length

    def split_edge(self, char, index):
        # Splits edges differently depending on whether it is a leaf or from an internal edge
        if self.is_leaf():
            # Leaf splitting creates a new node and edge and places the leaf
            new_node = Node()
            new_edge = Edge(self.start_index, char, self.parent)
            new_edge.end_index = index - 1
            self.child = new_node
            new_node.insert(self, char)

            self.start_index = index
            self.parent = new_node
            self.character = char
        else:
            new_edge = Edge(index, self.end_index, self.parent)
            new_edge.child = self.child
            new_node = Node()
            new_node.insert(new_edge, char)
            self.end_index = index - 1
            self.child = new_node


class Node:
    def __init__(self):
        self.suffix_link = None
        self.children = [None for _ in range(36, 127)]

    def __getitem__(self, item):
        return self.children[ord(item) - 36]

    def set_suffix_link(self, linked_node):
        self.suffix_link = linked_node

    def insert(self, edge_leaf, char):
        self.children[ord(char) - 36] = edge_leaf


def length_remainder(start, end):
    return end - start + 1


def suffix_tree(string):
    # active data
    n = len(string)
    root = Node()
    active_node = root
    root.set_suffix_link(root)
    remainder_start_index = 0
    remainder_end_index = -1
    global_end = GlobalEnd()
    node_created = False

    last_j = -1
    for i in range(n):
        for j in range(last_j + 1, i + 1):
            active_edge = active_node[string[remainder_start_index]]
            # Rule 2: create edge from node with no edge for the extension character
            if active_edge == None:
                # Creates new leaf and inserts into active node
                new_leaf = Edge(i, string[i], active_node)
                new_leaf.end_index = global_end
                active_node.insert(new_leaf, string[i])
                if node_created:
                    node_created.set_suffix_link(active_node)
                    node_created = False
                if active_node == root:
                    # maintain remainder length but move along
                    remainder_start_index += 1
                    remainder_end_index += 1
                active_node = active_node.suffix_link
                last_j += 1

            if active_edge is not None:
                # Skip count to active node
                if not active_edge.is_leaf():
                    remainder = length_remainder(remainder_start_index, remainder_end_index)
                    while len(active_edge) <= remainder:
                        active_node = active_edge.child
                        remainder_start_index += len(active_edge)
                        active_edge = active_node[string[remainder_start_index]]
                        if active_edge is None or active_edge.is_leaf():
                            break

            if active_edge is not None:
                # On an edge and need to go to extension point
                extension_point = active_edge.start_index + length_remainder(remainder_start_index, remainder_end_index)

                if string[extension_point] != string[i]:
                    # Splits the edge and creates a new node
                    active_edge.split_edge(string[extension_point], extension_point)

                    if active_edge.is_leaf():
                        if node_created:
                            node_created.set_suffix_link(active_edge.parent)
                        node_created = active_edge.parent
                    elif not active_edge.is_leaf():
                        if node_created:
                            node_created.set_suffix_link(active_edge.child)
                        node_created = active_edge.child
                    new_leaf = Edge(i, string[i], node_created)
                    node_created.insert(new_leaf, string[i])
                    if active_node == root:
                        remainder_start_index += 1
                    active_node = active_node.suffix_link
                    last_j += 1

                else:
                    # Rule 3 showstopper
                    if node_created:
                        node_created.set_suffix_link(active_node)
                        node_created = False
                    remainder_end_index += 1
                    break
        global_end.increment_end()
    return root


def st_to_sa(node, suffix_array):
    n = len(node.children)
    # Children array is lexicographic so loop through
    for i in range(n):
        tree_object = node.children[i]
        if tree_object is not None:
            # If leaf add index
            if tree_object.is_leaf():
                suffix_array.append(tree_object.start_index)
            else:
                # tree object is leaf, so it's child is a node
                # recurse deeper until we reach a leaf
                st_to_sa(tree_object.child, [])
    return suffix_array


def readfile(filepath):
    f = open(filepath, 'r')
    line = f.read()
    f.close()
    return line


def writefile(lst, filename):
    with open(filename, 'w') as f:
        f.write(str(len(lst)) + '\n')
        for item in lst:
            f.write(str(item) + '\n')


if __name__ == '__main__':
    _, txt_file = sys.argv
    input_str = readfile(txt_file)
    appended_dollar = input_str + '$'
    tree = suffix_tree(appended_dollar)
    sa = st_to_sa(tree, [])
    writefile(sa, 'output_sa.txt')

