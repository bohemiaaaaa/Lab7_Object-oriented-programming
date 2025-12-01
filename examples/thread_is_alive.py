#!/usr/bin/env python3
# -*- coding: utf-8 -*


from threading import Thread
from time import sleep


def func():
    for i in range(5):
        print(f"from child thread: {i}")
        sleep(0.5)


th = Thread(target=func)
print(f"thread status: {th.is_alive()}")

th.start()
print(f"thread status: {th.is_alive()}")

sleep(5)
print(f"thread status: {th.is_alive()}")
