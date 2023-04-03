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
    reverse_matching_str = pat[::-1] + '$' + txt[::-1]
    z_values = z_algorithm(matching_str)[m:]
    reverse_z_values = z_algorithm(reverse_matching_str)[m:][::-1]
    print(z_values)
    print(reverse_z_values)
    for i in range(len(z_values) - m + 1):
        # exact match case
        if z_values[i] == m:
            # +1 for 1 indexing
            matches.append(i + 1)
        # start transpose case
        # elif reverse_z_values[i + m - 1] == m - 2:
        #     if txt[i] == pat[1] and txt[i+1] == pat[0]:
        #         matches.append((i + 1, i + 1))
        # # end transpose case
        # elif z_values[i] == m - 2:
        #     if txt[i + m - 2] == pat[-1] and txt[i + m - 1] == pat[-2]:
        #         matches.append((i + 1, i + m - 1))
        # middle transpose case
        elif z_values[i] + reverse_z_values[i + m - 1] == m - 2:
            if txt[i + z_values[i]] == pat[z_values[i] + 1] and \
                    txt[i + m - 1 - reverse_z_values[i + m - 1]] \
                    == pat[m - reverse_z_values[i + m - 1] - 2]:
                # +1 for 1 indexing
                matches.append((i + 1, i + z_values[i] + 1))
    return matches


def compare(string, comp_start_index, start_of_txt_index=0):
    matches = 0
    while (comp_start_index < len(string)) and (string[comp_start_index] == string[start_of_txt_index]):
        matches += 1
        start_of_txt_index += 1
        comp_start_index += 1
    return matches
