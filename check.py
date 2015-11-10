#encoding:utf-8
"""
Created on 15/11/10
@author: zhuhui
"""

import threading
import copy
import re
import urllib, urllib2
import time


class Check:
    _checkUrl = "http://1111.ip138.com/ic.asp"
    def __init__(self):
        """
        :type self.proxies: list
        """
        self.proxies = None
        self.mutex = threading.Lock()
        self.timeOut = 5
        self.threadCount = 10
        self._idx = 0
        self.match = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}")
        self.successProxies = []

    def check(self, proxies):
        """
        :param proxies: 代理列表 形式: xxx.xxx.xxx.xxx:xxxx
        :return: 可用的代理列表
        """
        self.proxies = copy.copy(proxies)
        self.successProxies = []

        threadList = []
        for i in xrange(self.threadCount):
            th = threading.Thread(target=self.work)
            th.start()
            threadList.append(th)

        for th in threadList:
            th.join()

        return self.successProxies


    def work(self):
        while True:
            self.mutex.acquire()
            try:
                proxy = self.proxies.pop(0)
            except IndexError:
                return
            finally:
                self.mutex.release()

            if self.match.match(proxy):
                proxyHandle = urllib2.ProxyHandler({"http":"http://"+proxy})
                opener = urllib2.build_opener(proxyHandle)
                urllib2.install_opener(opener)

                t = time.clock()
                try:
                    resp = urllib2.urlopen(Check._checkUrl, timeout=self.timeOut).read()
                except:
                    resp = None
                finally:
                    t = time.clock() - t

                if resp:
                    m = re.search(r"\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]", resp)
                    self.mutex.acquire()
                    try:
                        if m.group(1) in proxy:
                            print "%s\t成功 -- %f秒" % (proxy, t)
                            self.successProxies.append(proxy)
                        else:
                            print "%s\t失败!!!!!!" % proxy
                    finally:
                        self.mutex.release()






