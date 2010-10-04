# Copyright (c) 2010 Matej Laitl <matej@laitl.cz>
# Distributed under the terms of the GNU General Public License v2 or any
# later version of the license, at your option.

"""Tests for numpywrap"""

import unittest as ut

from numpy import array, eye

import pybayes.numpywrap as nw
from support import approx_eq


class TestNumpywrap(ut.TestCase):

    def test_dot(self):
        A = array([[1., 2.], [3., -4.]])
        B = array([[2., 1.], [3.,  2.]])
        x = array([-4., -7.])

        AB = array([[ 8.,  5.], [-6., -5.]])
        BA = array([[ 5.,  0.], [ 9., -2.]])
        Ax = array([-18.,  16.])
        Bx = array([-15., -26.])

        for (left, right, exp) in [(A, B, AB), (B, A, BA), (A, x, Ax), (B, x, Bx)]:
            res = nw.dot(left, right)
            self.assertTrue(approx_eq(res, exp), "Arrays {0} and {1} are not fuzzy equal"
                .format(res, exp))

        A = array([[1., -0.5], [1., 0.]])
        R = array([[200., 0.], [0., 200.]])
        R = nw.dot(nw.dot(A, R), A.T)
        R_exp = array([[250., 200.], [200., 200.]])
        self.assertTrue(approx_eq(R, R_exp), "{0} is not fuzzy equal {1}"
            .format(R, R_exp))

    def test_inv(self):
        arrays = [
            array([[ 2.]]),
            array([[ 0.,  2.], [ 3.,  0.]]),
            array([[ 1., -2.], [-4.,  9.]]),
            array([[10., 11.], [100., 111.]]),  # near singular
            array([[1., 2., -3.], [1., -2., 3.], [-1., 2., 3.]])
        ]

        for A in arrays:
            iA = nw.inv(A)
            E = eye(A.shape[0])
            E1 = nw.dot(A, iA)
            E2 = nw.dot(iA, A)
            self.assertTrue(approx_eq(E1, E), "A = {0}\n".format(A) +
                "(A * inv(A)) = {0}\n".format(E1) +
                "which is not (fuzzy) identity!")
            self.assertTrue(approx_eq(E2, E), "A = {0}\n".format(A) +
                "(inv(A) * A) = {0}\n".format(E2) +
                "which is not (fuzzy) identity!")
