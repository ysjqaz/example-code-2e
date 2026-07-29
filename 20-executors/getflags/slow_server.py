#!/usr/bin/env python3

"""慢速 HTTP 服务器类。

本模块实现了一个 ThreadingHTTPServer，使用自定义的
SimpleHTTPRequestHandler 子类，对所有 GET 响应引入延迟，
并在传入 --error_rate 命令行参数时按比例返回错误响应。
"""

import contextlib
import os
import socket
import time
from functools import partial
from http import server, HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from random import random, uniform

MIN_DELAY = 0.5  # do_GET 的最短延迟（秒）
MAX_DELAY = 5.0  # do_GET 的最长延迟（秒）

class SlowHTTPRequestHandler(SimpleHTTPRequestHandler):
    """SlowHTTPRequestHandler 为测试 HTTP 客户端而加入延迟和错误。

    可选的 error_rate 参数决定 GET 请求收到 418 状态码
    "I'm a teapot" 的频率。
    例如 error_rate 为 .15 时，每个 GET 请求有 15% 的概率收到该错误。
    当服务器认为自己是茶壶时，会拒绝提供文件服务。

    See: https://tools.ietf.org/html/rfc2324#section-2.3.2
    """

    def __init__(self, *args, error_rate=0.0, **kwargs):
        self.error_rate = error_rate
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """处理一个 GET 请求。"""
        delay = uniform(MIN_DELAY, MAX_DELAY)
        cc = self.path[-6:-4].upper()
        print(f'{cc} delay: {delay:0.2}s')
        time.sleep(delay)
        if random() < self.error_rate:
            # HTTPStatus.IM_A_TEAPOT 需要 Python >= 3.9
            try:
                self.send_error(HTTPStatus.IM_A_TEAPOT, "I'm a Teapot")
            except BrokenPipeError as exc:
                print(f'{cc} *** BrokenPipeError: client closed')
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                except BrokenPipeError as exc:
                    print(f'{cc} *** BrokenPipeError: client closed')
                finally:
                    f.close()

# 下面 if 块中的代码（包括注释）复制自 Python 3.9 的
# `http.server` 模块并作了少量改动
# https://github.com/python/cpython/blob/master/Lib/http/server.py

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                             '[default:current directory]')
    parser.add_argument('--error-rate', '-e', metavar='PROBABILITY',
                        default=0.0, type=float,
                        help='Error rate; e.g. use .25 for 25%% probability '
                             '[default:0.0]')
    parser.add_argument('port', action='store',
                        default=8001, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8001]')
    args = parser.parse_args()
    handler_class = partial(SlowHTTPRequestHandler,
                            directory=args.directory,
                            error_rate=args.error_rate)

    # 确保不禁用双栈；参考 #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # 协议为 IPv4 时抑制异常
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    # test 是 http.server 中的顶层函数，未列入 __all__
    server.test(  # type: ignore
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
