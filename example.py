#coding:utf-8
__author__ = '30213'
'''
http://xlambda.com/gevent-tutorial
数据结构例子
'''

import gevent
from gevent.event import Event

'''
gevent.sleep(n)
只是为了模拟真实情况下的网络阻塞
'''

'''xxxx'''
class Example0(object):
    print ' -example0- ' * 10

    def __init__(self):
        pass



'''Event事件'''
class Example1(object):
    print ' -example1- ' * 10

    def __init__(self):
        self.evt = Event()
        self.main()

        pass

    def setter(self):
        print u'A:wait for me,'
        gevent.sleep(3)
        print 'OK,I\'m done'
        # todo: 设置异步等待
        self.evt.set()

    def waiter(self):
        print 'I\'ll wait for you!'
        # todo:
        self.evt.wait()
        print "It's about time,I will go.."

    def main(self):
        gevent.joinall([
            gevent.spawn(self.setter),
            gevent.spawn(self.waiter),
            gevent.spawn(self.waiter),
            gevent.spawn(self.waiter),
            gevent.spawn(self.waiter),
            gevent.spawn(self.waiter)
        ])
# Example1()


#TODO: 还未完全理解明白
'''队列'''
from gevent.queue import Queue
class Example2(object):
    print ' -example2- ' * 10

    def __init__(self):
        self.tasks = Queue()
        self.main()


    def worker(self,n):
        while not self.tasks.empty():
            task = self.tasks.get()
            print 'Worker %s got task %s'%(n,task)
            gevent.sleep(0)
        print 'Quitting time!'

    def boss(self):
        for i in xrange(1,25):
            self.tasks.put_nowait(i)

    def main(self):
        gevent.spawn(self.boss).join()
        # todo:不明白 join() 使用
        print 'yes,boss() is done!'
        gevent.joinall([
            gevent.spawn(self.worker,'steve'),
            gevent.spawn(self.worker,'john'),
            gevent.spawn(self.worker,'nancy'),
        ])

Example2()



