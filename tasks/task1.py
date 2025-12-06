#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import math
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Tuple


def series_term(n: int, x: float) -> float:
    try:
        denominator = (2 * n - 1) * (x ** (2 * n - 1))
        return 1.0 / denominator
    except OverflowError:
        return 0.0


def control_value(x: float) -> float:
    return 0.5 * math.log((x + 1) / (x - 1))


@dataclass
class ChunkResult:
    start_n: int
    end_n: int
    partial_sum: float
    terms_count: int


def calculate_chunk(
    start_n: int, end_n: int, x: float, epsilon: float, stop_flag: threading.Event
) -> ChunkResult:
    partial_sum = 0.0
    terms_count = 0

    for n in range(start_n, end_n + 1):
        if stop_flag.is_set():
            break

        term = series_term(n, x)

        if term == 0.0 or abs(term) < epsilon:
            stop_flag.set()
            break

        partial_sum += term
        terms_count += 1

    return ChunkResult(
        start_n=start_n,
        end_n=start_n + terms_count - 1,
        partial_sum=partial_sum,
        terms_count=terms_count,
    )


def calculate_series(
    x: float, epsilon: float, num_threads: int = 4
) -> Tuple[float, int]:
    stop_flag = threading.Event()

    chunk_size = 100

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        next_n = 1

        for i in range(num_threads * 2):
            if stop_flag.is_set():
                break

            end_n = next_n + chunk_size - 1
            future = executor.submit(
                calculate_chunk, next_n, end_n, x, epsilon, stop_flag
            )
            futures.append(future)
            next_n = end_n + 1

        total_sum = 0.0
        total_terms = 0
        completed_chunks = 0

        for future in as_completed(futures):
            if stop_flag.is_set() and completed_chunks > 0:
                break

            try:
                result = future.result()
                total_sum += result.partial_sum
                total_terms += result.terms_count
                completed_chunks += 1

                if not stop_flag.is_set() and result.terms_count < chunk_size:
                    stop_flag.set()

            except Exception as e:
                print(f"Ошибка при вычислении блока: {e}")

    return total_sum, total_terms


def main() -> None:
    x = 3.0
    epsilon = 1e-7

    print("Вычисление суммы бесконечного ряда с использованием многопоточности")
    print("=" * 60)

    S, terms_count = calculate_series(x, epsilon)
    print(f"Сумма бесконечного ряда S = {S:.10f}")
    print(f"Вычислено членов ряда: {terms_count}")

    y = control_value(x)
    print(f"\nКонтрольное значение y = {y:.10f}")

    print("\nСравнение полученной суммы с контрольным значением:")
    print(f"|S - y| = {abs(S - y):.2e}")

    if abs(S - y) < epsilon:
        print(f"Точность достигнута: |S - y| < ε = {epsilon}")
    else:
        print(f"Точность не достигнута: |S - y| ≥ ε = {epsilon}")


if __name__ == "__main__":
    main()
