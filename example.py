#coding:utf-8
__author__ = '30213'

import time
import gevent
import random

from gevent import select,Greenlet

start = time.time()
tic = lambda : 'at %1.1f seconds '%(time.time() - start)


''' 理解 joinall 的意义'''
class Example1(object):
    print ' -example1- '*10

    def __init__(self):
        # gevent.joinall()     #TODO 等待所有greenlet完成
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


'''理解同步与异步的不同'''
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


'''加深理解 joinall 和 spawn'''
class Example3(object):
    print ' -example3- '*10
    def __init__(self):
        thread1 = Greenlet.spawn(self.foo,u'该 协程1 只会执行1s',1)
        thread2 = gevent.spawn(self.foo,u'该 协程2 会在上个显示1s后显示',2)
        # TODO  不明白为什么 thread3 会在thread1 后执行
        thread3 = gevent.spawn(self.foo,u'这个 协程3 附带着玩的',1)
        gevent.joinall([thread1,thread2]) # TODO 等待所有greenlet完成
        print u'测试上面协程阻塞时，该信息是否会立即显示'

    def foo(self,message,n):
        startTime = time.time()
        gevent.sleep(n)
        endTime = time.time() - startTime
        print message,u'--验证结果--> 该协程运行时间:%s'%endTime
# Example3()


'''重载Greenlet类'''
class MyGreenlet(Greenlet):
    print ' -example4- '*10
    def __init__(self,message,n):
        Greenlet.__init__(self)
        self.message = message
        self.n = n
    # TODO 重写_run方法
    def _run(self):
        print self.message
        gevent.sleep(self.n)

def example4():
    g = MyGreenlet('Hi there',3)
    g.start()
    g.join()

# example4



class Example5(object):
    print ' -example5- '*10
    def __init__(self):
        winner = gevent.spawn(self.win)
        loser = gevent.spawn(self.fail)
        # TODO: started表示的Greenlet是否已经开始,返回布尔值
        print winner.started
        print loser.started

        try:
            gevent.joinall([winner,loser]) # 将会报错，由于 fail() 函数本身就会报错
        except Exception as e:
            print 'this will never be reached,Error:',e

    # 获取函数值, 这步 有可能比 try...except 快
        print 'winner.value:',winner.value
        print 'loser.value:',loser.value   # 由于异常，此处是 None，获取值在下面会得到

    # 测试是否已停止 Greenlet 的布尔值
        print 'winner.ready():',winner.ready()  #true
        print 'loser.ready():',loser.ready()    #true

    # 测试是否已经成功停止 Greenlet
        print 'winner.successful():',winner.successful()    #true
        print 'loser.successful():',loser.successful()      #False
    # TODO :打印异常报错信息
        print 'loser.exception:',loser.exception

    def win(self):
        return 'Your Win!'

    def fail(self):
        raise Exception('You fail at failing.')

    @classmethod
    def isStart(cls,*args,**kwargs):
        pass

# Example5()



'''gevent Timeout用法，以及 try...except... 新的理解'''
from gevent import Timeout

class Example6(object):
    print ' -example6- ' * 10

    def __init__(self):
        pass
        self.timeout(5)
        # TODO: try...except 只会执行其中一步，另外一步就默认不走，与 if ...else... 一样
        try:
            gevent.spawn(self.wait,5).join()  # todo :wait() 睡眠时间比 timeout() 低，就只会执行 try 语句
        except Timeout:
            print 'could not complete'

        try:
            gevent.spawn(self.wait,3).join()  # todo :wait() 睡眠时间比 timeout() 低，就只会执行 try 语句
        except Timeout:
            print 'could not complete'

    def timeout(self,n=5):
        timeout = Timeout(n)
        timeout.start()


    def wait(self,n=5):
        gevent.sleep(n)

Example6()