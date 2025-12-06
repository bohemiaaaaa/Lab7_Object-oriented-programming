import math
from queue import Queue

import pytest
from task1 import (
    SeriesThread,
    ThreadResult,
    calculate_series,
    control_value,
    series_term,
)


def test_series_term():
    assert pytest.approx(series_term(1, 3.0), rel=1e-12) == 1 / (1 * 3**1)
    assert pytest.approx(series_term(2, 3.0), rel=1e-12) == 1 / (3 * 3**3)


def test_series_term_overflow():
    assert series_term(1, 1e308) == 1e-308


def test_control_value():
    x = 3.0
    expected = 0.5 * math.log((x + 1) / (x - 1))
    assert pytest.approx(control_value(x), rel=1e-12) == expected


def test_series_thread_execution():
    q = Queue()
    t = SeriesThread(
        thread_id=1,
        x=3.0,
        epsilon=1e-7,
        start_n=1,
        end_n=5,
        result_queue=q,
    )
    t.start()
    t.join()

    res: ThreadResult = q.get()
    assert res.thread_id == 1
    assert res.start_n == 1
    assert res.end_n >= 1
    assert res.partial_sum > 0
    assert res.terms_count > 0


def test_calculate_series_basic():
    S, terms = calculate_series(3.0, 1e-7, num_threads=4)
    y = control_value(3.0)
    assert abs(S - y) < 1e-5
    assert terms > 0


def test_calculate_series_single_thread():
    S1, t1 = calculate_series(3.0, 1e-7, num_threads=1)
    S4, t4 = calculate_series(3.0, 1e-7, num_threads=4)
    assert isinstance(S1, float)
    assert isinstance(S4, float)
    assert t1 > 0
    assert t4 > 0
