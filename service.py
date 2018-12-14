#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Link 
@contact: zheng.long@shoufuyou.com
@module: service.py 
@date: 2018-12-14
@usage:
$>nameko run service --broker amqp://guest:guest@localhost
$>nameko shell --broker amqp://guest:guest@localhost
"""
import yagmail
from nameko.rpc import rpc, RpcProxy


class Mail(object):
    name = "mail"

    @rpc
    def send(self, to, subject, contents):
        yag = yagmail.SMTP(
            user='data.admin@shoufuyou.com',
            password='1A2b3cAdmin',
            host="smtp.exmail.qq.com",
            port=465
        )
        # 以上的验证信息请从安全的地方进行读取
        # 贴士: 可以去看看 Dynaconf 设置模块
        yag.send(to=to,
                 subject=subject,
                 contents=[contents])


class Compute(object):
    name = "compute"
    mail = RpcProxy('mail')

    @rpc
    def compute(self, operation, value, other, email):
        operations = {'sum': lambda x, y: int(x) + int(y),
                      'mul': lambda x, y: int(x) * int(y),
                      'div': lambda x, y: int(x) / int(y),
                      'sub': lambda x, y: int(x) - int(y)}
        try:
            result = operations[operation](value, other)
        except Exception as e:
            # 异步调用
            self.mail.send.call_async(email, "An error occurred", str(e))
            # self.mail.send(email, "An error occurred", str(e))
            raise
        else:
            self.mail.send.call_async(
                email,
                "Your operation is complete!",
                "The result is: %s" % result
            )
            return result


if __name__ == '__main__':
    pass

