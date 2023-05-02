# Author: Zachary Huggins
# ID: 30577012

class LeafNode:
    # Leaf of tree, has no set last char due to it always being the global end
    def __init__(self, start_char, char, suffix_label, parent):
        self.suffix_label = suffix_label
        self.parent = parent
        self.character = char
        self.start_idx = start_char

    def split_node_edge(self, char, idx):
        # create new edge and node
        # add edges child_link as the new node
        node = Node()
        edge = EdgeLink(idx - 1, self.start_idx)
        self.parent.insert_element(edge, self.character)
        edge.set_child_link(node)
        node.insert_element(self, char)

        self.start_idx = idx
        self.parent = node
        self.character = char


class EdgeLink:
    # Edge class that links parent node to children
    # Placed in parent's node Array
    child_link = None

    def __init__(self, end_char, start_char):
        self.start_idx = start_char
        self.end_idx = end_char

    def __len__(self):
        return self.end_idx - self.start_idx + 1

    def split_node_edge(self, char, idx):
        edge = EdgeLink(self.end_idx, idx)
        edge.set_child_link(self.child_link)
        node = Node()
        node.insert_element(edge, char)
        self.end_idx = idx - 1
        self.set_child_link(node)

    def set_child_link(self, child_node):
        self.child_link = child_node


class Node:

    suffix_link = None

    def __init__(self):
        # set array to be 92 in length due to amount of different characters possible (from ord($) to last ascii value)
        # one element for each possible child of a given node
        self.child_array = 92 * [None]

    def __getitem__(self, char):
        # Minus ord by 36 as ord($) = 36, so $ will always be at the index 0, keeping lexicographical ordering
        index = ord(char) - 36
        return self.child_array[index]

    def insert_element(self, element, char):
        # Same as get item but place the edge/leaf in the array
        index = ord(char) - 36
        self.child_array[index] = element

    def set_suffix_link(self, connecting_node):
        self.suffix_link = connecting_node


# Main algorithm utilising above classes
def ukkonen(aString):
    strLen = len(aString)
    treeRoot = Node()
    treeRoot.suffix_link = treeRoot
    last_j = -1
    new_node_created = False
    remainder_start = 0
    remainder_end = -1
    active_node = treeRoot

    def remainderLen():
        return remainder_end - remainder_start + 1

    for i in range(strLen):  # For loop == phases
        currChar = aString[i]
        for j in range(last_j + 1, i+1): # For loop for extension from last j to i
            currEdge = active_node[aString[remainder_start]]
            # utlising inbuilt get item function
            # current edge can be a leaf or an edge

            if currEdge:
                if type(currEdge) is EdgeLink:
                    while len(currEdge) <= remainderLen():
                        active_node = currEdge.child_link
                        remainder_start += len(currEdge)
                        currEdge = active_node[aString[remainder_start]]
                        if not currEdge or type(currEdge) is not EdgeLink:
                            break

            # active node is above extension point, then move to extension point if there is an curr_edge
            if currEdge:
                ext_point = currEdge.start_idx + remainderLen()

                if aString[ext_point] != currChar:
                    # when the new char doesn't match next, and not currently at node
                    # rule 2: case 2, split edge with new node
                    currEdge.split_node_edge(aString[ext_point], ext_point)
                    if type(currEdge) is EdgeLink:
                        if new_node_created:
                            new_node_created.set_suffix_link(currEdge.child_link)
                        new_node_created = currEdge.child_link
                    elif type(currEdge) is LeafNode:
                        if new_node_created:
                            new_node_created.set_suffix_link(currEdge.parent)
                        new_node_created = currEdge.parent
                    created_leaf = LeafNode(i, currChar, j, new_node_created)
                    new_node_created.insert_element(created_leaf, currChar)
                    if active_node == treeRoot:
                        # reduce remainder (space between remainder_end and remainder_start
                        remainder_start += 1
                    # Change active node
                    active_node = active_node.suffix_link
                    last_j += 1

                else:
                    # no mismatch
                    # rule 3
                    if new_node_created:  # for no suffix link specified
                        new_node_created.set_suffix_link(active_node)
                        new_node_created = False
                    remainder_end += 1
                    break  # stop due to rule 3

            else:
                # If at node and there is no edge to next char
                # rule 2: case 1
                # create new leaf with char and add it to the active node
                created_leaf = LeafNode(i, currChar, j, active_node)
                active_node.insert_element(created_leaf, currChar)
                if new_node_created:  # for no suffix link specified
                    new_node_created.set_suffix_link(active_node)
                    new_node_created = False
                if active_node == treeRoot:
                    # maintain length but increase remainder
                    remainder_start += 1
                    remainder_end += 1
                active_node = active_node.suffix_link
                last_j += 1

    # return root, since all nodes can be accessed from the root
    return treeRoot
