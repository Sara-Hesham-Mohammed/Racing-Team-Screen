from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time

class A:
    def run(self,text):
        print(f'{text}')

    def fakeFunc(self):
        print(f'OML')
        time.sleep(30)

class B:
    def run(self):
        print('hello')

    def fakeFunc(self, sleepTime):
        time.sleep(sleepTime)
        print(f'OH MA GOD {sleepTime}')




if __name__ == "__main__":
    a = A()
    b = B()

    pool = ThreadPoolExecutor(6)
    #task submission result can be stored in var
    pool.submit(a.run, 'hello world, this func A')#submitting task to the pool
    pool.submit(a.fakeFunc)#submitting task to the pool
    pool.submit(b.run)#submitting task to the pool
    pool.submit(b.fakeFunc, 10)#submitting task to the pool

    pool.shutdown(wait=True)