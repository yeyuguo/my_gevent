#coding:utf-8
__author__ = '30213'

import time
import gevent
import random

from gevent import select,Greenlet

'''xxxx'''
class Example0(object):
    print ' -example0- ' * 10

    def __init__(self):
        pass




''' 理解 joinall 的意义'''
class Example1(object):
    print ' -example1- '*10

    def __init__(self):
        start = time.time()
        self.tic = lambda : 'at %1.1f seconds '%(time.time() - start)
        # gevent.joinall()     #TODO 等待所有greenlet完成
        gevent.joinall([
            gevent.spawn(self.gr1),
            gevent.spawn(self.gr2),
            gevent.spawn(self.gr3),
            gevent.spawn(self.gr4)
        ])
    def gr1(self):
        print
        print 'gr1 started polling: ',self.tic();
        select.select([],[],[],2)
        print 'gr1 end polling: ',self.tic();

    def gr2(self):
        print 'gr2 started polling: ',self.tic();
        select.select([],[],[],2)
        print 'gr2 end polling: ',self.tic();

    def gr3(self):
        print 'gr3 started polling: ',self.tic();
        select.select([],[],[],2)
        print 'gr3 end polling: ',self.tic();

    def gr4(self):
        print "Hey lets do some stuff while the greenlets poll, at", self.tic()
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
        #TODO 在超时后，就会引起异常错误，否则不会报错
        self.timeout(5)    # todo:异步执行
        # TODO: try...except 只会执行其中一步，另外一步就默认不走，与 if ...else... 一样
        try:
            '''执行这步'''
            print u'执行try'
            gevent.spawn(self.wait,3).join()  # todo :wait() 睡眠时间比 timeout() 低，就只会执行 try 语句
        except Timeout:
            print u'执行 except'
            print 'could not complete'

        try:
            print u'执行try'
            gevent.spawn(self.wait,5).join()  # todo :wait() 睡眠时间比 timeout() 低，就只会执行 try 语句
        except Timeout:
            '''执行这步'''
            print u'执行 except'
            print 'could not complete'

    def timeout(self,n=5):
        timeout = Timeout(n)
        timeout.start()

    def wait(self,n=5):
        gevent.sleep(n)

# Example6()


''' with 处理上下文'''
class Example7(object):
    print ' -example7- ' * 10

    def __init__(self):
        # time_to_wait = 2
        # class TooLong(Exception):
        #     pass
        # with Timeout(time_to_wait, TooLong):
        #     gevent.sleep(5)

        time_to_wait = 5
        class TooLong(Exception):
            pass
        # TODO: 在超时后，就会引起异常错误，否则不会报错
        with Timeout(time_to_wait, TooLong):
            gevent.sleep(2)

# Example7()


import socket
from gevent import monkey
import select

'''Monkey patching 猴子补丁
    URL : http://xlambda.com/gevent-tutorial/#monkey-patching
    1.在极端情况下当一个库需要修改Python本身 的基础行为的时候，猴子补丁就派上用场了。
    2.gevent能够 修改标准库里面大部分的阻塞式系统调用，包括socket、ssl、threading和 select等模块，而变为协作式运行,
'''
class Example8(object):
    print ' -example8- ' * 10

    def __init__(self):
        pass
        print '-' * 10
        print 'socket.socket:',socket.socket
        print 'after monkey patch'
        monkey.patch_socket()
        print 'socket.socket:',socket.socket

        print '-' * 10
        print 'select.select:',select.select
        print 'after monkey patch'
        monkey.patch_select()
        print 'select.select:',select.select
# Example8()






