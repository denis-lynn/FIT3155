# Implementation of Boyer-Moore

def alphabet_index(letter):
    return ord(letter) - ord("a")


def compare(string, comp_char_index, prefix_index=0):
    matches = 0
    while (comp_char_index < len(string)) and (string[comp_char_index] == string[prefix_index]):
        matches += 1
        prefix_index += 1
        comp_char_index += 1
    return matches


def z_algorithm(txt):
    n = len(txt)
    z_values = []
    left = 0
    right = 0
    k = 1

    while k < n:
        # base case
        if k == 1:
            res = compare(txt, k)
            if res == 0:
                z_values.append(res)
            else:
                left, right = 1, res
                z_values.append(res)
        # case 1
        elif k > right:
            res = compare(txt, k)
            if res == 0:
                z_values.append(res)
            else:
                z_values.append(res)
                left, right = k, k + res - 1
        # case 2
        elif k <= right:
            prev_z_value = k - left - 1
            prev_right_distance = right - k + 1
            if z_values[prev_z_value] < prev_right_distance:
                z_values.append(z_values[prev_z_value])
            else:
                res = compare(txt, right + 1, prev_right_distance)
                z_values.append(prev_right_distance + res)
                left, right = k, right + res
        k += 1
    return z_values


def bad_character_preprocess(pat):
    pat_len = len(pat)
    bad_character_table = [[] for _ in range(26)]
    for i in range(pat_len - 1, -1, -1):
        bad_character_table[alphabet_index(pat[i])].append(i)
    return bad_character_table


def good_suffix_preprocess(pat):
    m = len(pat)
    gs_arr = [0 for _ in range(m + 1)]
    reverse_z_values = z_algorithm(pat[::-1])
    z_suffix_values = reverse_z_values[::-1]
    for i in range(m - 1):
        j = m - z_suffix_values[i]
        gs_arr[j] = i
    return gs_arr


def match_prefix_preprocess(pat):
    m = len(pat)
    mp_arr = [m]
    for i in range(m):
        mp_arr.append(0)
    z_values = z_algorithm(pat)
    longest_suffix = 0
    for i in range(len(z_values) - 1, -1, -1):
        if z_values[i] > longest_suffix:
            longest_suffix = z_values[i]
        mp_arr[i + 1] = longest_suffix
    return mp_arr


def bm_bc_shift(ch, bc_table, k):
    # max shift is 1 indexed
    shift = k + 1
    bc_vals = bc_table[alphabet_index(ch)]
    for i in range(len(bc_vals)):
        if bc_vals[i] < k:
            shift = k - bc_vals[i]
            break
    return shift


def bm_gs_shift(m, gs_table, k):
    return m - gs_table[k + 1] - 1


def bm_mp_shift(m, mp_table, k):
    return m - mp_table[k + 1]


def boyer_moore(txt, pat):
    # preprocessing
    bc_table = bad_character_preprocess(pat)
    gs_arr = good_suffix_preprocess(pat)
    mp_arr = match_prefix_preprocess(pat)

    n = len(txt)
    m = len(pat)

    # Pointers to text and pattern for comparison
    txt_pat_lineup_index = m - 1
    pat_compare_index = m - 1

    # Galil Optimisation Pointers
    start = -1
    stop = -1

    matches_arr = []

    # Outer loop
    while txt_pat_lineup_index < n:
        txt_compare_index = txt_pat_lineup_index

        while txt[txt_compare_index] == pat[pat_compare_index]:
            if pat_compare_index == 0:
                # +1 for 1 indexing
                matches_arr.append(txt_compare_index + 1)
                break

            txt_compare_index -= 1
            pat_compare_index -= 1

            if pat[pat_compare_index] == stop:
                galil_shift = stop - start
                pat_compare_index = max(start, 0)
                txt_compare_index -= galil_shift

        mismatch_char_txt = txt[txt_compare_index]
        bc_shift = bm_bc_shift(mismatch_char_txt, bc_table, pat_compare_index)
        if pat_compare_index + 1 == m:
            gs_shift = 1
        elif gs_arr[pat_compare_index + 1] == 0:
            gs_shift = bm_mp_shift(m, mp_arr, pat_compare_index)
            stop = mp_arr[pat_compare_index + 1] - 1
            start = 0
        else:
            gs_shift = bm_gs_shift(m, gs_arr, pat_compare_index)
            stop = gs_arr[pat_compare_index + 1] - 1
            start = gs_arr[pat_compare_index + 1] - m + pat_compare_index + 1

        shift = max(bc_shift, gs_shift)
        if shift != gs_shift:
            stop = -1
            start = -1

        txt_pat_lineup_index += shift
        pat_compare_index = m - 1

    return matches_arr
