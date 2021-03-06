"""The WaveBlocks Project

This file contains the interface for general quadrature rules.
Do not confuse quadratures with quadrature rules! Quadrature rules
are structs containing just nodes and weights and some convenience
methods. Quadratures are classes that really can compute things
like inner products (brakets) etc.

@author: R. Bourquin
@copyright: Copyright (C) 2010, 2011, 2012, 2013, 2014 R. Bourquin
@license: Modified BSD License
"""

__all__ = ["QuadratureRule"]


class QuadratureRule(object):
    r"""This class is an abstract interface to quadrature rules in general.
    """

    def __init__(self):
        r"""General interface for quadrature rules.
        :raise: :py:class:`NotImplementedError` Abstract interface.
        """
        raise NotImplementedError("'QuadratureRule' is an abstract interface.")


    def __str__(self):
        raise NotImplementedError("'QuadratureRule' is an abstract interface.")


    def __getitem__(self, key):
        r"""Handle quadrature rule options.
        """
        if key in self._options:
            return self._options[key]
        else:
            return None


    def get_description(self):
        r"""Return a description of this quadrature rule object.
        A description is a ``dict`` containing all key-value pairs
        necessary to reconstruct the current instance. A description
        never contains any data.
        """
        raise NotImplementedError("'QuadratureRule' is an abstract interface.")


    def get_dimension(self):
        r""":return: The space dimension :math:`D` of the quadrature rule.
        """
        return self._dimension


    def get_number_nodes(self):
        r"""

        :return: The number of quadrature nodes denoted by :math:`|\Gamma|` that are
                 part of this quadrature rule :math:`\Gamma = (\gamma, \omega)`.
        """
        return self._number_nodes


    def get_nodes(self):
        r"""

        :return: A two-dimensional ndarray containing the quadrature nodes :math:`\gamma_i`.
                 The array must have a shape of :math:`(D, |\Gamma|)`.
        """
        raise NotImplementedError("'QuadratureRule' is an abstract interface.")


    def get_weights(self):
        r"""

        :return: A two-dimensional ndarray containing the quadrature weights :math:`\omega_i`.
                 The array must have a shape of :math:`(1, |\Gamma|)`.
        """
        raise NotImplementedError("'QuadratureRule' is an abstract interface.")
