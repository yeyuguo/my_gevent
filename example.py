#coding:utf-8
__author__ = '30213'
'''
http://xlambda.com/gevent-tutorial
数据结构例子
'''

import gevent
from gevent.event import Event



'''xxxx'''
class Example0(object):
    print ' -example0- ' * 10

    def __init__(self):
        pass



'''Event事件'''
class Example1(object):
    print ' -example1- ' * 10

    def __init__(self):
        pass

    def setter(self):
        print u'A:wait for me,'
        gevent.sleep(3)
        print 'OK,I\'m done'


