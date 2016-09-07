#coding:utf-8
__author__ = '30213'

import time
import gevent
import random

from gevent import select

start = time.time()
tic = lambda : 'at %1.1f seconds '%(time.time() - start)


# 理解 joinall 的意义
class Example1(object):
    print ' -example1- '*10

    def __init__(self):

        gevent.joinall([
            gevent.spawn(self.gr1),
            gevent.spawn(self.gr2),
            gevent.spawn(self.gr3),
            gevent.spawn(self.gr4)
        ])
    def gr1(self):
        print
        print 'gr1 started polling: ',tic();
        select.select([],[],[],2)
        print 'gr1 end polling: ',tic();

    def gr2(self):
        print 'gr2 started polling: ',tic();
        select.select([],[],[],2)
        print 'gr2 end polling: ',tic();

    def gr3(self):
        print 'gr3 started polling: ',tic();
        select.select([],[],[],2)
        print 'gr3 end polling: ',tic();

    def gr4(self):
        print "Hey lets do some stuff while the greenlets poll, at", tic()
        gevent.sleep(1)
# Example1()


# 理解同步与异步的不同
class Example2():
    print ' -example2- '*10

    def __init__(self):
        print 'synchronous:'
        self.synchronous()

        print 'asynchronous'
        self.asynchronous()

    def task(self,pid):
        gevent.sleep(random.randint(0,2)*0.001)
        print 'Task:%s done'%pid

    def synchronous(self):
        for i in range(1,10):
            self.task(i)

    def asynchronous(self):
        threads = [gevent.spawn(self.task,i) for i in xrange(10) ]
        gevent.joinall(threads)

# Example2()




