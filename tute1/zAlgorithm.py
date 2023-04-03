# Implementation of Gusfield's Z algorithm
# distance = end - start + 1

def naive_z_algorithm(txt):
    n = len(txt)
    z_values = []
    for i in range(1, n):
        num_matches = compare(txt, i)
        z_values.append(num_matches)
    return z_values


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


def z_pattern_matching(txt, pat):
    m = len(pat)
    matches = []
    matching_str = pat + '$' + txt
    z_values = z_algorithm(matching_str)
    for i in range(len(z_values)):
        if z_values[i] == m:
            # +1 for 1 indexing
            matches.append(i - m + 1)
    return matches


def compare(string, comp_start_index, start_of_txt_index=0):
    matches = 0
    while (comp_start_index < len(string)) and (string[comp_start_index] == string[start_of_txt_index]):
        matches += 1
        start_of_txt_index += 1
        comp_start_index += 1
    return matches
