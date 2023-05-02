# suffix array is First column of cyclic rotations of string
def naive_suffix_array(string):
    n = len(string)
    suffix_array = []
    for i in range(n):
        suffix_array.append((string[i:], i))
    sorted_suffixes = sorted(suffix_array)
    for i in range(n):
        suffix_array[i] = sorted_suffixes[i][1]
    print(sorted_suffixes)
    return suffix_array


# index in string = n - len(suffix)
def naive_suffix_array2(string):
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
        bwt += string[suffix_array[i]-1]
    return bwt


print(naive_suffix_array2('banana$'))
# print(bwt_from_suffix_array(naive_suffix_array2('googol$'), 'googol$'))
print(bwt_from_suffix_array(naive_suffix_array2('banana$'), 'banana$'))
