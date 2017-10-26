from multiprocessing import Process, Queue, Pool
import random
import os
import time

def f(x):
    taskid = os.getpid()
    print('Run task {}'.format(taskid))
    start = time.time()
    if x % 2:
        y = x
    else:
        y = 'Even'
        try:
            f.q.put(x)
        except:
            pass
    time.sleep(1)
    end = time.time()
    print('Task {} runs {:.2f} seconds.'.format(taskid, end - start))
    return y

def f_init(q):
    # This is a monkey patch, which allows us to modify the
    # attributes in run time. Also, methods in python are also objects,
    # which allows this f.q operation
    f.q = q

if __name__ == '__main__':
    print('Parent process: {}'.format(os.getpid()))
    start = time.time()
    q = Queue()
    # Initializer will be applied to each process in the pool
    with Pool(processes=4, initializer=f_init, initargs=[q]) as p:
        print(p.map(f, range(4)))
    print('Even list: {}'.format([q.get() for i in range(q.qsize())]))
    print('Multiprocessing. Time: {}'.format(time.time() - start))
    start = time.time()
    print(list(map(f, range(4))))
    print('Asynchronous. Time: {}'.format(time.time() - start))