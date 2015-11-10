#encoding:utf-8
"""
Created on 15/11/10
@author: zhuhui
"""

from check import Check

someProxies = """
182.254.153.54:80
117.177.243.53:8080
39.171.108.213:8123
117.177.243.15:8080
180.208.78.49:80
222.88.236.236:843
58.220.2.141:80
58.220.2.140:80
120.198.236.10:80
58.220.2.136:80
58.220.2.133:80
222.88.236.234:81
202.194.96.46:80
180.97.185.35:10001
58.220.2.142:80
116.228.80.186:8080
220.248.224.242:8089
58.220.2.135:80
115.159.5.247:80
111.12.83.27:80
106.38.251.62:8088
203.148.12.132:8000
"""

if __name__ == "__main__":
    ck = Check()
    successProxies = ck.check(someProxies.split('\n'))
    print "\n".join(successProxies)