from Queue import Queue
from threading import Thread


class Worker(Thread):

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()


class ThreadPool:

    def __init__(self, thread_num):
        self.tasks = Queue(thread_num)
        for _ in range(thread_num):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()

# use:
# def func(var):
#   print(var)
#
# pool = ThreadPool(2)
# pool.add_task(func, 4)
# pool.add_task(func, "hi")
# pool.wait_completion()
