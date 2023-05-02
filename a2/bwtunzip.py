import sys


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = ''
        self.bit_symbol = ''


def elias_omega_decoder(bitstring):
    component_msb_index = 0
    component_end_index = 0

    while bitstring[component_msb_index] != '1':
        component = bitstring[component_msb_index:component_end_index + 1]
        read_len = len(component)
        # Flip msb by adding most significant bit
        flipped_msb_component = int(component, 2) + 2 ** (read_len - 1)
        new_len = flipped_msb_component + 1
        component_end_index = component_end_index + new_len
        component_msb_index = component_end_index - new_len + 1

    data_component = bitstring[component_msb_index:component_end_index + 1]
    int_data_component = int(data_component, 2)
    return int_data_component, component_end_index + 1


def read_bin_file(filepath):
    f = open(filepath, 'rb')
    binary_data = f.read()
    return binary_data


def conv_byte_to_bits(binary_data):
    bitstring = ''
    # it seems that python does a bit of from_bytes action already if we iterate over the binary data
    for b in binary_data:
        bitstring += format(b, '08b')
    return bitstring


def decode_header(bitstring):
    next_decode_index = 0
    # Get length of bwt and increment along the bitstring
    bwt_len, decode_incrementer = elias_omega_decoder(bitstring)
    next_decode_index += decode_incrementer
    # Get number of unique characters and increment along the bitstring
    no_uniq_chars, decode_incrementer = elias_omega_decoder(bitstring[next_decode_index:])
    next_decode_index += decode_incrementer
    # Loop over seven bit ascii, code len and huffman code
    leaf_nodes = []
    for _ in range(no_uniq_chars):
        # Recover Ascii and turn into char
        ascii_in_bits = bitstring[next_decode_index: next_decode_index + 7]
        ascii_in_int = int(ascii_in_bits, 2)
        ascii_in_char = chr(ascii_in_int)
        next_decode_index += 7
        # Recover code_len
        code_len, decode_incrementer = elias_omega_decoder(bitstring[next_decode_index:])
        next_decode_index += decode_incrementer
        # Recover code and place data into leaf nodes, so we can rebuild tree
        huffman_code = bitstring[next_decode_index:next_decode_index+code_len]
        next_decode_index += len(huffman_code)
        leaf_nodes.append((ascii_in_char, huffman_code))
    return leaf_nodes, bitstring[next_decode_index:], bwt_len


def reconstruct_huffman_tree(leaf_nodes):
    root = Node()
    for i in range(len(leaf_nodes)):
        traverse_reconstruct(root, leaf_nodes[i][1], leaf_nodes[i][0])
    return root


def traverse_reconstruct(node, huffman_code, char):
    if huffman_code == '':
        node.data = char
        return node
    if huffman_code[0] == '0' and not node.left:
        node.left = Node()
        traverse_reconstruct(node.left, huffman_code[1:], char)
    if huffman_code[0] == '0' and node.left:
        traverse_reconstruct(node.left, huffman_code[1:], char)
    if huffman_code[0] == '1' and not node.right:
        node.right = Node()
        traverse_reconstruct(node.right, huffman_code[1:], char)
    if huffman_code[0] == '1' and node.right:
        traverse_reconstruct(node.right, huffman_code[1:], char)


def print_tree_lol(node, level=0):
    if node is not None:
        print_tree_lol(node.right, level + 1)
        print(' ' * 4 * level + '-> ' + str(node.data))
        print_tree_lol(node.left, level + 1)


def traverse_tree(node, data, char_code, huffman_code=''):
    new_huffman_code = huffman_code

    if not node.left and not node.right:
        char_code.append(node.data)
        char_code.append(new_huffman_code)

    if data[0] == '0':
        traverse_tree(node.left, data[1:], char_code, new_huffman_code)
    if data[0] == '1':
        traverse_tree(node.right, data[1:], char_code, new_huffman_code)

    return char_code


# def decode_data(root, data_in_bits, str_len):
#     n = len(data_in_bits)
#     is_huffman = True
#     decode_next_index = 0
#     while str_len > 0
#         if is_huffman:









if __name__ == '__main__':
    _, bin_file = sys.argv
    bin_data = read_bin_file(bin_file)
    bit_string = conv_byte_to_bits(bin_data)
    decoded_nodes, remainder_to_decode, bwt_len = decode_header(bit_string)
    # print(remainder_to_decode)
    reconstructed_tree = reconstruct_huffman_tree(decoded_nodes)
    # print_tree_lol(reconstructed_tree)
    print(traverse_tree(reconstructed_tree, remainder_to_decode, []))
