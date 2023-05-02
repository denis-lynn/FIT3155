import sys


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


def transposition(txt, pat):
    m = len(pat)
    matches = []
    matching_str = pat + '$' + txt
    reverse_matching_str = pat[::-1] + '$' + txt[::-1]
    z_values = z_algorithm(matching_str)[m:]
    reverse_z_values = z_algorithm(reverse_matching_str)[m:][::-1]
    for i in range(len(z_values) - m + 1):
        # exact match case
        if z_values[i] == m:
            # +1 for 1 indexing
            matches.append(str(i + 1))
        # middle transpose case
        elif z_values[i] + reverse_z_values[i + m - 1] == m - 2:
            if txt[i + z_values[i]] == pat[z_values[i] + 1] and \
                    txt[i + m - 1 - reverse_z_values[i + m - 1]] \
                    == pat[m - reverse_z_values[i + m - 1] - 2]:
                # +1 for 1 indexing
                matches.append(str(i + 1) + ' ' + str(i + z_values[i] + 1))
    return matches


def compare(string, comp_char_index, prefix_index=0):
    matches = 0
    while (comp_char_index < len(string)) and (string[comp_char_index] == string[prefix_index]):
        matches += 1
        prefix_index += 1
        comp_char_index += 1
    return matches


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
    _, txt_file, pat_file = sys.argv
    txt_content = readfile(txt_file)
    pat_content = readfile(pat_file)
    results = transposition(txt_content, pat_content)
    writefile(results, "output_q1.txt")
