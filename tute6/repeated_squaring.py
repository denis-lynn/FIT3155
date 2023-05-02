def repeated_squaring(a: int, b: int, n: int) -> int:
    binary = format(b, 'b')
    reversed_bin = binary[::-1]
    res = 1
    prev_mod_val = 0
    # loop through length of binary number for repeated squaring
    for i in range(len(reversed_bin)):
        # Calculate square based on previous mod value
        if i == 0:
            prev_mod_val = a % n
        else:
            prev_mod_val = (prev_mod_val ** 2) % n
            # Update result when binary at pos is 1
            if reversed_bin[i] == '1':
                res = (res * prev_mod_val) % n
    return res


print(repeated_squaring(7, 330, 13))




