#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
import threading

import pytest
from task1 import (
    calculate_chunk,
    calculate_series,
    control_value,
    series_term,
)


def test_series_term_basic():
    assert math.isclose(series_term(1, 3), 1 / (1 * 3**1))
    assert math.isclose(series_term(2, 3), 1 / (3 * 3**3))
    assert math.isclose(series_term(3, 3), 1 / (5 * 3**5))


def test_series_term_overflow_safe():
    assert series_term(10_000, 3) == 0.0


def test_control_value():
    x = 3.0
    expected = 0.5 * math.log((x + 1) / (x - 1))
    assert math.isclose(control_value(x), expected)


def test_calculate_chunk_basic():
    x = 3.0
    epsilon = 1e-7
    stop_flag = threading.Event()

    result = calculate_chunk(1, 50, x, epsilon, stop_flag)

    assert result.partial_sum > 0
    assert result.terms_count > 0
    assert result.end_n >= result.start_n


def test_calculate_chunk_stop_on_epsilon():
    x = 3.0
    epsilon = 1e-3
    stop_flag = threading.Event()

    result = calculate_chunk(1, 1000, x, epsilon, stop_flag)

    assert result.terms_count < 1000
    assert stop_flag.is_set()


def test_calculate_series_accuracy():
    x = 3.0
    epsilon = 1e-7

    S, terms = calculate_series(x, epsilon)
    y = 0.5 * math.log((x + 1) / (x - 1))

    assert abs(S - y) < epsilon
    assert terms > 0


def test_calculate_series_small_threads():
    x = 3.0
    epsilon = 1e-7

    S1, t1 = calculate_series(x, epsilon, num_threads=1)
    S4, t4 = calculate_series(x, epsilon, num_threads=4)

    assert math.isclose(S1, S4, rel_tol=1e-7)


def test_calculate_series_fast_stop():
    x = 3.0
    epsilon = 1e-2

    S, terms = calculate_series(x, epsilon)

    assert terms < 10
    assert abs(S - control_value(x)) < 1e-2


def test_calculate_chunk_raises_on_invalid_args():
    with pytest.raises(TypeError):
        calculate_chunk("invalid", 10, 3.0, 1e-7, threading.Event())
