#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module containing useful general functions that don't belong to another
module.

"""
__revision__ = "$Revision$"

import math
import numpy as np
from scipy.special import erfc
#import math.erf
# erf can also be found in the scipy.special library
# erf can also be found in the math library -> python 2.7 ou above
# erf can also be found in the mpmath library


def peig(A, n):
    """Returns a matrix whose columns are the `n` dominant eigenvectors
    of `A` (eigenvectors corresponding to the `n` dominant
    eigenvalues).

    Parameters
    ----------
    A : 2D numpy array
        A symmetric matrix (bi-dimensional numpy array).
    n : int
        Number of desired dominant eigenvectors.

    Returns
    -------
    [V, D] : list
        A list with two elements where the first element is a 2D numpy
        array with the desired eigenvectors, while the second element is a
        1D numpy array with the corresponding eigenvalues.

    Notes
    -----
    `A` must be a symmetric matrix so that its eigenvalues are real and
    positive.

    Raises
    ------
    ValueError
        If `n` is greater than the number of columns of `A`.

    Examples
    --------
    >>> A = np.random.randn(3,3) + 1j*np.random.randn(3,3)
    >>> V, D = peig(A, 1)

    """
    (_, ncols) = A.shape
    if n > ncols:  # Since A is symmetric we could get either nrows or ncols
        raise ValueError("`n` must be lower then the number of columns in `A`")

    [D, V] = np.linalg.eig(A)
    indexes = np.argsort(D.real)
    indexes = indexes[::-1]
    V = V[:, indexes[0:n]]
    D = D[indexes[0:n]]
    return [V, D]


def leig(A, n):
    """Returns a matrix whose columns are the `n` least significant
    eigenvectors of `A` (eigenvectors corresponding to the `n` dominant
    eigenvalues).

    Parameters
    ----------
    A : 2D numpy array
        A symmetric matrix (bi-dimensional numpy array)
    n : int
        Number of desired least significant eigenvectors.

    Returns
    -------
    [V, D] : list
        A list with two elements where the first element is a 2D numpy
        array with the desired eigenvectors, while the second element is a
        1D numpy array with the corresponding eigenvalues.

    Notes
    -----
    `A` must be a symmetric matrix so that its eigenvalues are real and
    positive.

    Raises
    ------
    ValueError
        If `n` is greater than the number of columns of `A`.

    Examples
    --------
    >>> A = np.random.randn(3,3) + 1j*np.random.randn(3,3)
    >>> V, D = peig(A, 1)

    """
    (_, ncols) = A.shape
    if n > ncols:  # Since A is symmetric we could get either nrows or ncols
        raise ValueError("`n` must be lower then the number of columns in `A`")

    [D, V] = np.linalg.eig(A)
    indexes = np.argsort(D.real)
    V = V[:, indexes[0:n]]
    D = D[indexes[0:n]]
    return [V, D]


def pretty_time(time_in_seconds):
    """Return the time in a more friendly way.

    Parameters
    ----------
    time_in_seconds : float
        Time in seconds.

    Returns
    -------
    time_string : str
        Pretty time representation as a string.

    Examples
    --------
    >>> pretty_time(30)
    '30.00s'
    >>> pretty_time(76)
    '1m:16s'
    >>> pretty_time(4343)
    '1h:12m:23s'
    """
    seconds = time_in_seconds
    minutes = int(seconds) / 60
    seconds = int(round(seconds % 60))

    hours = minutes / 60
    minutes = minutes % 60

    if(hours > 0):
        return "%sh:%sm:%ss" % (hours, minutes, seconds)
    elif(minutes > 0):
        return "%sm:%ss" % (minutes, seconds)
    else:
        return "%.2fs" % time_in_seconds


def xor(a, b):
    """Calculates the xor operation between a and b.

    In python this is performed with a^b. However, sage changed the "^"
    operator. This xor function was created so that it can be used in
    either sage or in regular python.

    Parameters
    ----------
    a : int
        First number.
    b : int
        Second number.

    Returns
    -------
    result : int
        The result of the `xor` operation between `a` and `b`.

    Examples
    --------
    >>> xor(3,7)
    4
    >>> xor(15,6)
    9
    """
    return (a).__xor__(b)


def randn_c(*args):
    """Generates a random circularly complex gaussian matrix.

    Parameters
    ----------
    params : variable number of ints
        Variable number of arguments specifying the dimensions of the
        returned array. This is directly passed to the numpy.random.randn
        function.

    Returns
    -------
    result : N-dimensional numpy array
        A random N-dimensional numpy array (complex dtype) where the `N` is
        equal to the number of parameters passed to `randn_c`.

    Examples
    --------
    >>> a = randn_c(4,3)
    >>> a.shape
    (4, 3)
    >>> a.dtype
    dtype('complex128')

    """
    return (1.0 / math.sqrt(2.0)) * (
        np.random.randn(*args) + (1j * np.random.randn(*args)))


def level2bits(n):
    """Calculates the number of bits needed to represent n different
    values.

    Parameters
    ----------
    n : int
        Number of different levels.

    Returns
    -------
    num_bits : int
        Number of bits required to represent `n` levels.

    Examples
    --------
    >>> map(level2bits,range(1,20))
    [1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5]
    """
    if n < 1:
        raise ValueError("level2bits: n must be greater then one")
    return int2bits(n - 1)


def int2bits(n):
    """Calculates the number of bits needed to represent an interger n.

    Parameters
    ----------
    n : int
        The ingerger number.

    Returns
    -------
    num_bits : int
        The number of bits required to represent the number `n`.

    Examples
    --------
    >>> map(int2bits, range(0,19))
    [1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5]
    """
    if n < 0:
        raise ValueError("int2bits: n must be greater then zero")

    if n == 0:
        return 1

    bits = 0
    while n:
        n >>= 1
        bits += 1
    return bits


def _count_bits_single_element(n):
    """Count the number of bits that are set in an interger number.

    Parameters
    ----------
    n : int
        The interger number.

    Returns
    -------
    Number of bits that are equal to 1 in the bit representation of the
    number `n`.

    """
    count = 0
    while n > 0:
        if n & 1 == 1:
            count += 1
        n >>= 1
    return count
# Make count_bits an ufunc
# count_bits = np.frompyfunc(_count_bits_single_element, 1, 1,
#                            doc=_count_bits_single_element.__doc__)

count_bits = np.vectorize(_count_bits_single_element)


def qfunc(x):
    """Calculates the qfunction of x.

    Parameters
    ----------
    x : float
        The value to apply the Q function.

    Returns
    -------
    result : float
        Qfunc(x)

    Examples
    --------
    >>> qfunc(0.0)
    0.5
    >>> round(qfunc(1.0), 9)
    0.158655254
    >>> round(qfunc(3.0), 9)
    0.001349898
    """
    return 0.5 * erfc(x / math.sqrt(2))


def least_right_singular_vectors(A, n):
    """Return the three matrices. The first one is formed by the `n` least
    significative right singular vectors of `A`, the second one is formed
    by the remaining right singular vectors of `A` and the third one has
    the singular values of the singular vectors of the second matrix (the
    most significative ones).

    Parameters
    ----------
    A : 2D numpy array
        A 2D numpy array.
    n : int
        An interger between 0 and the number of columns of `A`.

    Returns
    -------
    V0 : 2D numpy array
        The right singular vectors corresponding to the `n` least
        significant singular values.
    V1 : 2D numpy array
        The remaining right singular vectors.
    S : 1D numpy array
        The singular values corresponding to the remaining singular vectors
        `V1`.

    Notes
    -----
    Because of the sort operation, if you call
    least_right_singular_vectors(A, ncols_of_A) you will get all the right
    singular vectors of A with the column order reversed.

    Examples
    --------
    >>> A = np.array([1,2,3,6,5,4,2,2,1])
    >>> A.shape = (3,3)
    >>> (min_Vs, remaining_Vs, S) = least_right_singular_vectors(A,1)
    >>> min_Vs
    array([[-0.4474985 ],
           [ 0.81116484],
           [-0.3765059 ]])
    >>> remaining_Vs
    array([[-0.62341491, -0.64116998],
           [ 0.01889071, -0.5845124 ],
           [ 0.78166296, -0.49723869]])
    >>> S
    array([ 1.88354706,  9.81370681])

    """
    # Note that numpy.linalg.svd returns the hermitian of V
    [_, S, V_H] = np.linalg.svd(A, full_matrices=True)

    V = V_H.conjugate().transpose()

    # Index in crescent order of the singular values

    # Since the SVD gives the values in decrescent order, we just need to
    # reverse the order instead of performing a full sort
    sort_indexes = [i for i in reversed(range(0, V.shape[0]))]
    #sort_indexes = S.argsort()

    # The `n` columns corresponding to the least significtive singular
    # values
    V0 = V[:, sort_indexes[0:n]]

    #(nrows, ncols) = V.shape
    V1 = V[:, sort_indexes[n:]]

    return (V0, V1, S[sort_indexes[n:]])


# New versions of numpy already have this method
# https://gist.github.com/1511969/222e3316048bce5763b1004331af898088ffcd9e
# def ravel_multi_index(indexes, shape):
#     """
#     Get the linear index corresponding to `indexes`.

#     The linear index is calculated in 'C' order. That is, it "travels"
#     the array faster in the fist dimension than in the last (row order
#     in bi-dimensional arrays).

#     Arguments
#     - `indexes`: A list with the indexes of each dimension in the array.
#     - `shape`: Shape of the array

#     Ex:
#     For shape=[3,3] we get the matrix
#     array([[0, 1, 2],
#            [3, 4, 5],
#            [6, 7, 8]])
#     Therefore (the indexes start at zero),
#     >>> ravel_multi_index([0,2],[3,3])
#     2

#     Similarly
#     >>> ravel_multi_index([3,1],[4,3])
#     10
#     """
#     #c order only
#     base_c = np.arange(np.prod(shape)).reshape(*shape)
#     return base_c[tuple(indexes)]


def calc_unorm_autocorr(x):
    """Calculates the unormalized autocorrelation of an array x starting from
    lag 0.

    Parameters
    ----------
    x : 1D numpy array
        A 1D numpy array.

    Returns
    -------
    result : 1D numpy array
        The unormalized autocorrelation of `x`.

    Examples
    --------
    >>> x = np.array([4, 2, 1, 3, 7, 3, 8])
    >>> calc_unorm_autocorr(x)
    array([152,  79,  82,  53,  42,  28,  32])

    """
    #R = np.convolve(x, x[::-1], 'full')
    R = np.correlate(x, x, 'full')

    # Return the autocorrelation for indexes greater then or equal to 0
    return R[R.size / 2:]


def calc_autocorr(x):
    """Calculates the (normalized) autocorrelation of an array x starting
    from lag 0.

    Parameters
    ----------
    x : 1D numpy array
        A 1D numpy array.

    Returns
    -------
    result : 1D numpy array
        The ormalized autocorrelation of `x`.

    Examples
    --------
    >>> x = np.array([4, 2, 1, 3, 7, 3, 8])
    >>> calc_autocorr(x)
    array([ 1.   , -0.025,  0.15 , -0.175, -0.25 , -0.2  ,  0.   ])
    """
    x2 = x - np.mean(x)
    variance = float(np.var(x2))  # Biased variance of x2

    # We divide by x2.size because the calculated variance is the biased
    # version. If it was the unbiased we would have to divide by x2.size-1
    # instead.
    return calc_unorm_autocorr(x2) / (x2.size * variance)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

if __name__ == '__main__':  # pragma: nocover
    import doctest
    doctest.testmod()
