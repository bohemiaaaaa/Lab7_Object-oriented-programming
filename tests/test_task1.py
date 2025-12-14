#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math

import pytest
from task1 import Series


def test_single_term_value():
    s = Series(x=3.0)
    term = s._compute_element(1)

    expected = 1.0 / ((2 * 1 - 1) * (3.0 ** (2 * 1 - 1)))
    assert math.isclose(term, expected, rel_tol=1e-12)


def test_analytical_value():
    s = Series(x=3.0)
    exact = s.analytical()

    expected = 0.5 * math.log((3.0 + 1) / (3.0 - 1))
    assert math.isclose(exact, expected, rel_tol=1e-12)


@pytest.mark.parametrize("threads", [1, 2, 4, 8])
def test_series_convergence(threads):
    eps = 1e-7
    s = Series(x=3.0, eps=eps)

    value, terms = s.evaluate(threads_num=threads)
    exact = s.analytical()

    assert abs(value - exact) < eps
    assert terms > 0


def test_result_stability():
    s = Series(x=3.0, eps=1e-7)

    value_2, _ = s.evaluate(threads_num=2)
    value_4, _ = s.evaluate(threads_num=4)

    assert abs(value_2 - value_4) < 1e-9


def test_terms_count_reasonable():
    s = Series(x=3.0, eps=1e-7)
    _, terms = s.evaluate(threads_num=4)

    assert 1 < terms < 10_000
