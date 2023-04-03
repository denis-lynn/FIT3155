from tute1 import zAlgorithm


def alphabet_index(letter):
    return ord(letter) - ord("a")


def bad_character_preprocess(pat):
    pat_len = len(pat)
    bad_character_table = []
    for i in range(26):
        bad_character_table.append([])
    for i in range(pat_len - 1, -1, -1):
        bad_character_table[alphabet_index(pat[i])].append(i)
    return bad_character_table


def good_suffix_preprocess(pat):
    pat_len = len(pat)
    gs_arr = []
    for i in range(pat_len + 2):
        gs_arr.append(0)
    z_values = zAlgorithm.z_algorithm(pat[::-1])
    z_suffix_values = z_values[::-1]
    for i in range(pat_len):
        j = pat_len - z_suffix_values[i] + 1
        gs_arr[j] = i
    return gs_arr
