from threading import Thread
from time import sleep

class CustomThread(Thread):
    def __init__(self, limit):
        Thread.__init__(self)
        self.limit_ = limit

    def run(self):
        for i in range(self.limit_):
            print(f"from CustomThread: {i}")
            sleep(0.5)

cth = CustomThread(3)
cth.start()

