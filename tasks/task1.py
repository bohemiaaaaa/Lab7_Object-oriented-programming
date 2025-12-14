#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from series import Series


def main() -> None:
    series = Series(x=3.0, eps=1e-7)

    print(series)

    s_value, terms_used = series.evaluate(threads_num=4)

    print(f"Сумма ряда S = {s_value:.10f}")
    print(f"Использовано членов ряда: {terms_used}")

    exact = series.analytical()
    print(f"Контрольное значение y = {exact:.10f}")
    print(f"|S - y| = {abs(s_value - exact):.2e}")

    if abs(s_value - exact) < series.eps:
        print("Точность достигнута")
    else:
        print("Точность не достигнута")


if __name__ == "__main__":
    main()
