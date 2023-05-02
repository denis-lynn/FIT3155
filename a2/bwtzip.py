import sys


class Node:
    def __init__(self, data, frequency):
        self.left = None
        self.right = None
        self.data = data
        self.frequency = frequency
        self.bit_symbol = ''


def naive_suffix_array(string):
    n = len(string)
    suffix_array = []
    for i in range(n):
        suffix_array.append(string[i:])
    sorted_suffixes = sorted(suffix_array)
    for i in range(n):
        suffix_array[i] = n - len(sorted_suffixes[i])
    return suffix_array


# BWT because of L precedes F is just i-1 of each index in suffix array
def bwt_from_suffix_array(suffix_array, string):
    bwt = ''
    n = len(suffix_array)
    for i in range(n):
        bwt += string[suffix_array[i] - 1]
    return bwt


def elias_omega_encoder(number):
    min_binary_code = format(number, 'b')
    res = min_binary_code
    while len(min_binary_code) > 1:
        n = len(min_binary_code)
        new_min_code_len = n - 1
        new_bit_len = new_min_code_len.bit_length()
        most_significant_bit_decimal = 2 ** (new_bit_len - 1)
        # Flip most significant bit by subtracting it from the new_bit_len
        # Pad the remaining zeroes
        min_binary_code = format(new_min_code_len - most_significant_bit_decimal, '0' + str(new_bit_len) + 'b')
        res = min_binary_code + res
    return res


def find_char_freq(string):
    # Alphabet Array includes 36 for $ which should always have frequency 1
    alphabet_arr = [0 for _ in range(36, 127)]
    leaf_nodes = []
    for char in string:
        alphabet_arr[ord(char) - 36] += 1
    for i in range(len(alphabet_arr)):
        if alphabet_arr[i] != 0:
            leaf_nodes.append(Node(chr(i + 36), alphabet_arr[i]))
    return leaf_nodes


def find_least_freq_char(list_of_nodes):
    minimum_freq_index = 0
    for index in range(len(list_of_nodes)):
        if list_of_nodes[index].frequency < list_of_nodes[minimum_freq_index].frequency:
            minimum_freq_index = index
    return minimum_freq_index


def huffman_tree_constructor(leaf_nodes):
    # Use constructed leaf_nodes list to construct huffman tree
    root = None
    if len(leaf_nodes) == 1:
        root = leaf_nodes[0]
        root.bit_symbol = '0'
    else:
        while len(leaf_nodes) > 1:
            least_freq_node_index = find_least_freq_char(leaf_nodes)
            least_freq_node = leaf_nodes.pop(least_freq_node_index)
            second_least_freq_node_index = find_least_freq_char(leaf_nodes)
            second_least_freq_node = leaf_nodes.pop(second_least_freq_node_index)
            combined_node = Node(least_freq_node.data + second_least_freq_node.data,
                                 least_freq_node.frequency + second_least_freq_node.frequency)
            combined_node.left = least_freq_node
            least_freq_node.bit_symbol = '0'
            combined_node.right = second_least_freq_node
            second_least_freq_node.bit_symbol = '1'
            leaf_nodes.append(combined_node)
        root = leaf_nodes[0]
    return root


def generate_huff_codes(node, huff_storer, huffman_code=''):
    new_huffman_code = huffman_code + str(node.bit_symbol)

    if node.left:
        generate_huff_codes(node.left, huff_storer, new_huffman_code)
    if node.right:
        generate_huff_codes(node.right, huff_storer, new_huffman_code)

    if not node.left and not node.right:
        huff_storer[ord(node.data) - 36] = new_huffman_code

    return huff_storer


def bwt_encoder(bwt):
    encoded_str = ''

    bwt_len = elias_omega_encoder(len(bwt))
    uniq_chars = find_char_freq(bwt)
    elias_uniq_chars = elias_omega_encoder(len(uniq_chars))
    encoded_str += bwt_len + elias_uniq_chars

    root = huffman_tree_constructor(uniq_chars)

    huff_codes_arr = generate_huff_codes(root, [None for _ in range(36, 127)])

    for i in range(len(huff_codes_arr)):
        if huff_codes_arr[i]:
            bit7_ascii = format(i + 36, '07b')
            huff_code_len_elias = elias_omega_encoder(len(huff_codes_arr[i]))
            huff_code = huff_codes_arr[i]
            # print(bit7_ascii, huff_code_len_elias, huff_code)
            encoded_str += bit7_ascii + huff_code_len_elias + huff_code

    i = 0
    while i < len(bwt):
        run_len = 1
        while i < len(bwt) - 1 and bwt[i] == bwt[i + 1]:
            run_len += 1
            i += 1
        curr_char_huff = huff_codes_arr[ord(bwt[i]) - 36]
        curr_char_run_len = elias_omega_encoder(run_len)
        encoded_str += curr_char_huff + curr_char_run_len
        i += 1
    return encoded_str


def write_to_bytes(bitstring, filename):
    f = open(filename, 'wb')
    n = len(bitstring)
    amount_to_pad = 8 - (n % 8)
    bitstring += '0' * amount_to_pad
    check = ''
    for i in range(0, n, 8):
        one_byte = int(bitstring[i:i + 8], 2).to_bytes(1, byteorder='big')
        f.write(one_byte)
    f.close()


def readfile(filepath):
    f = open(filepath, 'r')
    line = f.read()
    f.close()
    return line


if __name__ == '__main__':
    _, txt_file = sys.argv
    input_str = readfile(txt_file)
    appended_dollar = input_str + '$'
    bwt = bwt_from_suffix_array(naive_suffix_array(appended_dollar), appended_dollar)
    encoded_str = bwt_encoder(bwt)
    write_to_bytes(encoded_str, 'bwtencoded.bin')
