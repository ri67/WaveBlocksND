"""The WaveBlocks Project

Combinatorics functions for enumerating various objects.

@author: R. Bourquin
@copyright: Copyright (C) 2014 R. Bourquin
@license: Modified BSD License
"""

from numpy import zeros, integer, product
from scipy.special import binom


def multinomial(kv):
    r"""Compute the multinomial

    :param kv: The numbers downstairs in the multinomial notation.
    """
    return product([binom(sum(kv[:i + 1]), ki) for i, ki in enumerate(kv)])


def partitions(D, K):
    r"""Enumerate integer partitions in anti-lexicographic
    order for integers up to (and including) some limit K.
    All partitions have exactly D parts, some may be zero.

    :param D: Dimension
    :param K: Limit
    """
    P = zeros((D,), dtype=integer)

    yield P.copy()
    while P.sum() <= K:
        p0 = P[0]
        for i in range(1, D):
            p0 += P[i]
            if P[0] <= P[i] + 1:
                P[i] = 0
            else:
                P[0] = p0 - i * (P[i] + 1)
                P[1:(i + 1)] = P[i] + 1
                yield P.copy()
                break
        else:
            P[0] = p0 + 1
            if P.sum() <= K:
                assert P.sum() <= K
                yield P.copy()


def lattice_points_norm(D, N):
    r"""Enumerate all lattice points of an integer lattice
    :math:`\Lambda \subset \mathbb{N}^D` in :math:`D` dimensions
    having fixed :math:`l_1` norm :math:`N`.

    :param D: The dimension :math:`D` of the lattice.
    :param N: The :math:`l_1` norm of the lattice points.
    """
    k = zeros(D, dtype=integer)
    k[0] = N
    yield tuple(k)

    c = 1
    while k[D - 1] < N:
        if c == D:
            for i in range(c - 1, 0, -1):
                c = i
                if not k[i - 1] == 0:
                    break
        k[c - 1] = k[c - 1] - 1
        c += 1
        k[c - 1] = N - sum(k[0:c - 1])
        if c < D:
            k[c:D] = zeros(D - c, dtype=integer)

        yield tuple(k)


def lattice_points(D, N):
    r"""Enumerate all lattice points of an integer lattice
    :math:`\Lambda \subset \mathbb{N}^D` in :math:`D` dimensions
    having :math:`l_1` norm smaller or equal to :math:`N`.

    :param D: The dimension :math:`D` of the lattice.
    :param N: The maximal :math:`l_1` norm of the lattice points.
    """
    for n in range(N + 1):
        for l in lattice_points_norm(D, n):
            yield l


def permutations(P):
    r"""Enumerate all permutations in anti-lexicographical
    order follwing the given permutation `P`.

    :param P: A permutation
    :type P: An `ndarray` of shape `(D,)`
    """
    D = P.size
    P = P.copy()
    yield P.copy()
    while True:
        for i in range(1, D):
            pi = P[i]
            if P[i - 1] > pi:
                I = i
                if i > 1:
                    J = I
                    for j in range(I // 2):
                        pj = P[j]
                        if pj <= pi:
                            I = I - 1
                        P[j] = P[i - j - 1]
                        P[i - j - 1] = pj
                        if P[j] > pi:
                            J = j + 1
                    if P[I - 1] <= pi:
                        I = J
                P[i] = P[I - 1]
                P[I - 1] = pi
                yield P.copy()
                break
        else:
            raise StopIteration
