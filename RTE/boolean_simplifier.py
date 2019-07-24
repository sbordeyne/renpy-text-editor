"""
Implementation of the Quine-McCluskey boolean simplifier in python
"""

import math


class BooleanSimplifier:
    def __init__(self):
        pass

    def qm(self, ones=[], zeros=[], dc=[]):
        '''Compute minimal two-level sum-of-products form.
        Arguments are:
            ones: iterable of integer minterms
            zeros: iterable of integer maxterms
            dc: iterable of integers specifying don't-care terms

        For proper operation, either (or both) the 'ones' and 'zeros'
        parameters must be specified.  If one of these parameters is not
        specified, it will be computed from the combination of the other
        parameter and the optional 'dc' parameter.

        An assertion error will be raised if any terms are specified
        in more than one argument, or if all three arguments are given
        and not all terms are specified.'''

        elts = max(max(ones or zeros or dc),
                   max(zeros or dc or ones),
                   max(dc or ones or zeros)) + 1
        numvars = int(math.ceil(math.log(elts, 2)))
        elts = 1 << numvars
        all = set(self.b2s(i, numvars) for i in range(elts))
        ones = set(self.b2s(i, numvars) for i in ones)
        zeros = set(self.b2s(i, numvars) for i in zeros)
        dc = set(self.b2s(i, numvars) for i in dc)
        ones = ones or (all - zeros - dc)
        zeros = zeros or (all - ones - dc)
        dc = dc or (all - ones - zeros)
        assert len(dc) + len(zeros) + len(ones) == len(dc | zeros | ones) == elts
        primes = self.compute_primes(ones | dc, numvars)
        return self.unate_cover(primes, ones)


    def unate_cover(self, primes, ones):
        '''Return the minimal cardinality subset of primes covering all ones.

        Exhaustive for now.  Feel free to replace this with an efficient unate
        covering problem solver.'''

        primes = list(primes)
        cs = min((self.bitcount(self.b2s(cubesel, len(primes))), cubesel)
                 for cubesel in range(1 << len(primes))
                 if self.is_full_cover(self.active_primes(cubesel, primes), ones))[1]
        return self.active_primes(cs, primes)


    def active_primes(self, cubesel, primes):
        '''Return the primes selected by the cube selection integer.'''
        return [prime for used, prime in
                zip(map(int, self.b2s(cubesel, len(primes))), primes) if used]


    def is_full_cover(self, all_primes, ones):
        '''Return a bool: Does the set of primes cover all minterms?'''
        return min([max([self.is_cover(p, o) for p in all_primes] + [False])
                   for o in ones] + [True])


    def is_cover(self, prime, one):
        '''Return a bool: Does the prime cover the minterm?'''
        return min([p == 'X' or p == o for p, o in zip(prime, one)] + [True])


    def compute_primes(self, cubes, vars):
        '''Compute primes for the given set of cubes and variable count.'''
        sigma = [set(i for i in cubes if self.bitcount(i) == v)
                 for v in range(vars + 1)]
        primes = set()
        while sigma:
            nsigma = []
            redundant = set()
            for c1, c2 in zip(sigma[:-1], sigma[1:]):
                nc = set()
                for a in c1:
                    for b in c2:
                        m = self.merge(a, b)
                        if m:
                            nc.add(m)
                            redundant |= set([a, b])
                nsigma.append(nc)
            primes |= set(c for cubes in sigma for c in cubes) - redundant
            sigma = nsigma
        return primes


    def bitcount(self, s):
        '''Return the sum of on bits in s.'''
        return sum(b == '1' for b in s)


    def b2s(self, i, vars):
        '''Convert from an integer to a binary string.'''
        s = ''
        for k in range(vars):
            s = ['0', '1'][i & 1] + s
            i >>= 1
        return s


    def merge(self, i, j):
        '''Return cube merge.  'X' is don't-care.  'None' if merge impossible.'''
        s = ''
        dif_cnt = 0
        for a, b in zip(i, j):
            if (a == 'X' or b == 'X') and a != b:
                return None
            elif a != b:
                dif_cnt += 1
                s += 'X'
            else:
                s += a
            if dif_cnt > 1:
                return None
        return s
