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
        bwt += string[suffix_array[i] - 1]
    return bwt


<<<<<<< HEAD:tutes/tute3/bwt.py
def invert_bwt(bwt):
    n = len(bwt)
    alphabet = [0 for _ in range(36, 127)]
    no_occ = [0 for _ in range(n)]
    rank = [0 for _ in range(36, 127)]
    for i in range(n):
        no_occ[i] = alphabet[ord(bwt[i])-36]
        alphabet[ord(bwt[i])-36] += 1
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
        next_pos = rank[ord(bwt[i])-36]+no_occ[i]
        i = next_pos
    return reconstructed_str



print(invert_bwt('annb$aa'))
print(invert_bwt('lo$oogg'))

# print(naive_suffix_array2('banana$'))
=======
print(naive_suffix_array2('banana$'))
>>>>>>> 461920891b952182a57a7b7238e7dd9e2363311c:tute3/bwt.py
# print(bwt_from_suffix_array(naive_suffix_array2('googol$'), 'googol$'))
print(bwt_from_suffix_array(naive_suffix_array2('banana$'), 'banana$'))
