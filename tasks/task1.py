#!/usr/bin/env python3
# -*- coding: utf-8 -*


import math
import threading
from dataclasses import dataclass
from queue import Queue
from typing import Tuple


def series_term(n: int, x: float) -> float:
    """Вычисление n-го члена бесконечного ряда"""
    try:
        # Формула ряда: 1/((2n-1)*x^(2n-1))
        denominator = (2 * n - 1) * (x ** (2 * n - 1))
        return 1.0 / denominator
    except OverflowError:
        # Если слишком большая степень, член практически 0
        return 0.0


def control_value(x: float) -> float:
    """Контрольное значение функции"""
    # Формула: y = 0.5 * ln((x+1)/(x-1))
    return 0.5 * math.log((x + 1) / (x - 1))


@dataclass
class ThreadResult:
    """Результат работы потока"""

    thread_id: int
    start_n: int
    end_n: int
    partial_sum: float
    terms_count: int


class SeriesThread(threading.Thread):
    """Поток для вычисления части суммы ряда"""

    def __init__(
        self,
        thread_id: int,
        x: float,
        epsilon: float,
        start_n: int,
        end_n: int,
        result_queue: Queue,
    ):
        super().__init__()
        self.thread_id = thread_id
        self.x = x
        self.epsilon = epsilon
        self.start_n = start_n
        self.end_n = end_n
        self.result_queue = result_queue

    def run(self) -> None:
        """Основной метод потока"""
        partial_sum = 0.0
        terms_count = 0
        n = self.start_n

        # Вычисляем члены ряда в заданном диапазоне
        while n < self.end_n:
            term = series_term(n, self.x)

            # Проверка точности
            if term == 0.0 or abs(term) < self.epsilon:
                break

            partial_sum += term
            terms_count += 1
            n += 1

        # Сохраняем результат
        result = ThreadResult(
            thread_id=self.thread_id,
            start_n=self.start_n,
            end_n=n,
            partial_sum=partial_sum,
            terms_count=terms_count,
        )
        self.result_queue.put(result)


def calculate_series(
    x: float, epsilon: float, num_threads: int = 4
) -> Tuple[float, int]:
    """Многопоточное вычисление суммы ряда"""
    result_queue = Queue()
    threads = []

    # Каждый поток вычисляет по 50 членов ряда
    terms_per_thread = 50

    # Создаем и запускаем потоки
    for i in range(num_threads):
        start_n = i * terms_per_thread + 1
        end_n = start_n + terms_per_thread

        thread = SeriesThread(
            thread_id=i + 1,
            x=x,
            epsilon=epsilon,
            start_n=start_n,
            end_n=end_n,
            result_queue=result_queue,
        )
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()

    # Собираем результаты
    total_sum = 0.0
    total_terms = 0

    while not result_queue.empty():
        result = result_queue.get()
        total_sum += result.partial_sum
        total_terms += result.terms_count

    return total_sum, total_terms


def main() -> None:
    """Основная функция"""

    # Параметры из задания
    x = 3.0
    epsilon = 1e-7

    print("Вычисление суммы бесконечного ряда с использованием многопоточности")
    print("=" * 60)

    # Вычисляем сумму ряда (бесконечный ряд)
    S, terms_count = calculate_series(x, epsilon)
    print(f"Сумма бесконечного ряда S = {S:.10f}")
    print(f"Вычислено членов ряда: {terms_count}")

    # Вычисляем контрольное значение
    y = control_value(x)
    print(f"\nКонтрольное значение y = {y:.10f}")

    # Сравнение
    print("\nСравнение полученной суммы с контрольным значением:")
    print(f"|S - y| = {abs(S - y):.2e}")

    # Проверка точности
    if abs(S - y) < epsilon:
        print(f"Точность достигнута: |S - y| < ε = {epsilon}")
    else:
        print(f"Точность не достигнута: |S - y| ≥ ε = {epsilon}")


if __name__ == "__main__":
    main()
