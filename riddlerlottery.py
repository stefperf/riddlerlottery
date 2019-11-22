# https://fivethirtyeight.com/features/can-you-decode-the-riddler-lottery/

from functools import lru_cache, reduce
from itertools import combinations


@lru_cache(None)
def factorise(n):
    """
    given an integer n, return the ordered list of its prime factors, with repetitions
    :param n: int to be factorised
    :return: list of prime factors

    >>> factorise(12)
    [2, 2, 3]
    """
    fact = []
    i = 2
    while i <= n:
        if n % i == 0:
            fact.append(i)
            n //= i
        else:
            i += 1
    return fact


@lru_cache(None)
def prime_factors(n):
    """
    return the list of prime factors of n, without repetitions
    :param n: int to be factorised
    :return: list of prime factors

    >>> prime_factors(12)
    [2, 3]
    """
    fact = []
    i = 2
    while i <= n:
        if n % i == 0:
            if not fact or fact[-1] != i:
                fact.append(i)
            n //= i
        else:
            i += 1
    return fact


def count_occurrences(rep_list):
    """
    given a list with repetitions, return a dictionary of occurrence counts
    :param rep_list: list with possibly repeated elements
    :return: dictionary with elements as keys and occurrence counts as values

    >>> count_occurrences([2, 2, 3, 5, 5, 5])
    {2: 2, 3: 1, 5: 3}
    """
    occurrences = {}
    for factor in rep_list:
        occurrences[factor] = occurrences.get(factor, 0) + 1
    return occurrences


def listprod(li):
    return reduce((lambda x, y: x * y), li)


N = 70

print('\nSelection 1: keep only numbers with multiple prime factors:')
candidates1 = []
for n in range(1, N+1):
    if len(prime_factors(n)) >= 2:
        candidates1.append(n)
print('candidates1:')
for i, n in enumerate(candidates1, 1):
    print('%d: %d => %s' % (i, n, factorise(n)))

print('\nSelection 2: keep only numbers whose prime factors occur in at least 5 candidate numbers:')
prime_multiples1 = {}
for n in candidates1:
    for p in prime_factors(n):
        prime_multiples1.setdefault(p, []).append(n)
print('occorrences of primes:')
for prime, multiples in prime_multiples1.items():
    print('%d: %s' % (prime, multiples))
candidates2 = candidates1.copy()
for prime, multiples in prime_multiples1.items():
    if len(multiples) < 5:
        for m in multiples:
            if m in candidates2:
                candidates2.remove(m)
print('candidates2:')
for i, n in enumerate(candidates2, 1):
    print('%d: %d => %s' % (i, n, factorise(n)))
prime_totals2 = {}
for n in candidates2:
    for p in factorise(n):
        prime_totals2[p] = prime_totals2.get(p, 0) + 1
print('total counts of primes:')
for prime, count in prime_totals2.items():
    print('%d: %s' % (prime, count))

print('\nBrute-force search space:')
possible_combinations = {}
for i, comb in enumerate(combinations(candidates2, 25), 1):
    print('%d: %s' % (i, comb))
    all_factors = sorted(reduce((lambda l1, l2: l1 + l2), [factorise(n) for n in comb]))
    occurrences = count_occurrences(all_factors)
    possible = True
    for v in occurrences.values():
        if v % 5 != 0:
            possible = False
    if possible:
        possible_combinations[comb] = occurrences

print('\nPossible selections:')
for selection, occurrences in possible_combinations.items():
    product = 1
    for factor, factor_power in occurrences.items():
        product *= pow(factor, factor_power // 5)
    print('Total set = %s => each set product = %d' % (selection, product))

print('\nSubsets with desired product:')
for selection, occurrences in possible_combinations.items():
    product = 1
    for factor, factor_power in occurrences.items():
        product *= pow(factor, factor_power // 5)
    break
possible_sets = []
for comb in combinations(selection, 5):
    if reduce((lambda x, y: x * y), comb) == product:
        possible_sets.append(frozenset(comb))
for i, ps in enumerate(possible_sets, 1):
    print('%d: %s' % (i, sorted(ps)))
possible_partitions = set()
for set0 in possible_sets:
    curr_set = set0
    for set1 in possible_sets:
        if not curr_set.isdisjoint(set1):
            continue
        curr_set = curr_set.union(set1)
        for set2 in possible_sets:
            if not curr_set.isdisjoint(set2):
                continue
            curr_set = curr_set.union(set2)
            for set3 in possible_sets:
                if not curr_set.isdisjoint(set3):
                    continue
                curr_set = curr_set.union(set3)
                for set4 in possible_sets:
                    if not curr_set.isdisjoint(set4):
                        continue
                    possible_partition = frozenset([set0, set1, set2, set3, set4])
                    possible_partitions.add(possible_partition)
print('\nPossible partitions:')
for i, pp in enumerate(possible_partitions, 1):
    print('%d: %s' % (i, sorted([sorted(list(s)) for s in pp])))
