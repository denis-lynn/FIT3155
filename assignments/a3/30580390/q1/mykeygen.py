# Denis Lynn 30580390

import sys
import random


K_VALUE = 64


def modular_exp(a: int, b: int, n: int) -> int:
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


def miller_rabin(n: int, k: int):
    if n % 2 == 0:
        return False
    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2
    for _ in range(k):
        a = random.randint(2, n-1)
        # fermat's
        if modular_exp(a, n-1, n) != 1:
            return False
        prev_mod = modular_exp(a, t, n)
        # Checking on different a's
        for i in range(1, s+1):
            current_mod = modular_exp(a, (2**i)*t, n)
            congruent_to_one = current_mod == 1 % n
            prev_one = prev_mod == 1 % n
            prev_minus_one = prev_mod == -1 % n
            if congruent_to_one and not (prev_one or prev_minus_one):
                return False
            prev_mod = current_mod
    return True


def euclid(a: int, b: int):
    # mod based euclids
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a


def number_gen(d: int):
    res = 2 ** d - 1
    return res


def find_next_two_primes(d: int):
    p = 0
    q = 0
    curr_int = d
    while p == 0 or q == 0:
        temp = number_gen(curr_int)
        if miller_rabin(temp, K_VALUE):
            if p == 0:
                p = temp
            else:
                q = temp
        curr_int += 1
    return p, q


def find_exponent(p: int, q: int):
    first_term = p - 1
    second_term = q - 1
    gcd_terms = euclid(first_term, second_term)
    lam = (first_term * second_term)//gcd_terms
    exponent = random.randint(3, lam-1)
    while euclid(exponent, lam) != 1:
        exponent = random.randrange(3, lam-1)
    return exponent


def writefile(p, q, exponent):
    with open('publickeyinfo.txt', 'w') as f:
        f.write('# modulus (n)' + '\n')
        f.write(str(p*q) + '\n')
        f.write('# exponent (e)' + '\n')
        f.write(str(exponent))
    with open('secretprimes.txt', 'w') as g:
        g.write('# p' + '\n')
        g.write(str(p) + '\n')
        g.write('# q' + '\n')
        g.write(str(q))


if __name__ == '__main__':
    _, d1 = sys.argv
    p1, q1 = find_next_two_primes(int(d1))
    exp = find_exponent(p1, q1)
    writefile(p1, q1, exp)

