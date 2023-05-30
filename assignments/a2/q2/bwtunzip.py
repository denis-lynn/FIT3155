# Denis Lynn
# 30580390
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
        huffman_code = bitstring[next_decode_index:next_decode_index + code_len]
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


def traverse_tree(node, data, char_len_storer, traverse_len=0):
    new_traverse_len = traverse_len + 1

    if not node.left and not node.right:
        char_len_storer.append(node.data)
        char_len_storer.append(new_traverse_len)

    if data[0] == '0' and node.left:
        traverse_tree(node.left, data[1:], char_len_storer, new_traverse_len)
    if data[0] == '1' and node.right:
        traverse_tree(node.right, data[1:], char_len_storer, new_traverse_len)

    return char_len_storer


def decode_data(root, data_in_bits, str_len):
    is_huffman = True
    reconstructed_bwt = ''
    huffman_char = ''
    while str_len > 0:
        if is_huffman:
            char_len = traverse_tree(root, data_in_bits, [])
            huffman_char = char_len[0]
            len_read = char_len[1] - 1
            data_in_bits = data_in_bits[len_read:]
            is_huffman = False
        else:
            run_len, len_read = elias_omega_decoder(data_in_bits)
            data_in_bits = data_in_bits[len_read:]
            reconstructed_bwt += huffman_char * run_len
            str_len -= run_len
            is_huffman = True
    return reconstructed_bwt


def invert_bwt(bwt):
    # O(n) time complexity and space is bounded by Max(n, alphabet_size)
    # Alphabet size is coded to the spec of this assignment
    n = len(bwt)
    alphabet = [0 for _ in range(36, 127)]
    no_occ = [0 for _ in range(n)]
    rank = [0 for _ in range(36, 127)]
    for i in range(n):
        no_occ[i] = alphabet[ord(bwt[i]) - 36]
        alphabet[ord(bwt[i]) - 36] += 1
    first_rank_index = 0
    run_len = 0
    for i in range(len(alphabet)):
        if alphabet[i] != 0:
            first_rank_index += run_len
            rank[i] = first_rank_index
            run_len = alphabet[i]
    i = 0
    reconstructed_str = ''
    while bwt[i] != '$':
        reconstructed_str = bwt[i] + reconstructed_str
        next_pos = rank[ord(bwt[i]) - 36] + no_occ[i]
        i = next_pos
    return reconstructed_str


def writefile(string, filename):
    with open(filename, 'w') as f:
        f.write(string)


if __name__ == '__main__':
    _, bin_file = sys.argv
    bin_data = read_bin_file(bin_file)
    bit_string = conv_byte_to_bits(bin_data)
    decoded_nodes, remainder_to_decode, bwt_len = decode_header(bit_string)
    reconstructed_tree = reconstruct_huffman_tree(decoded_nodes)
    decoded_bwt = decode_data(reconstructed_tree, remainder_to_decode, bwt_len)
    res = invert_bwt(decoded_bwt)
    writefile(res, 'recovered.txt')
