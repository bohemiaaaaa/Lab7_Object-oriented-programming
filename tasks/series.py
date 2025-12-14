#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
from threading import Thread


class Series:
    def __init__(self, x: float = 3.0, eps: float = 1e-7) -> None:
        self.x = x
        self.eps = eps

    def _compute_element(self, n: int) -> float:
        try:
            return 1.0 / ((2 * n - 1) * (self.x ** (2 * n - 1)))
        except OverflowError:
            return 0.0

    def _thread_task(
        self,
        start_index: int,
        step: int,
        sums: list,
        counts: list,
        pos: int,
    ) -> None:
        partial_sum = 0.0
        elements_count = 0

        n = start_index
        term = self._compute_element(n)

        while abs(term) >= self.eps:
            partial_sum += term
            elements_count += 1

            n += step
            term = self._compute_element(n)

        sums[pos] = partial_sum
        counts[pos] = elements_count

    def evaluate(self, threads_num: int = 4) -> tuple[float, int]:
        workers = []
        partial_sums = [0.0] * threads_num
        elements_counts = [0] * threads_num

        for i in range(threads_num):
            t = Thread(
                target=self._thread_task,
                args=(i + 1, threads_num, partial_sums, elements_counts, i),
            )
            workers.append(t)
            t.start()

        for t in workers:
            t.join()

        return sum(partial_sums), sum(elements_counts)

    def analytical(self) -> float:
        return 0.5 * math.log((self.x + 1) / (self.x - 1))

    def __str__(self) -> str:
        return (
            "Ряд:\n"
            "S = Σ [ 1 / ((2n - 1) * x^(2n - 1)) ],  n = 1 .. ∞\n\n"
            f"x = {self.x}\n"
            f"epsilon = {self.eps}\n"
        )
