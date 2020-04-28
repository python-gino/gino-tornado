#!/usr/local/python/bin/python
# -*- coding: utf-8 -*-
"""
Gino-tornado app example
"""
# general imports

import queries
import logging

# tornado imports
import tornado
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.queues import Queue
from tornado.locks import Event
from tornado.options import define, parse_command_line, options

# local imports
from servers import build_service
from settings import DEBUG, SSL_OPTIONS, SSL_DEPLOY, OWN_DB_INFO
from models import db


@gen.coroutine
def launch_service(host='localhost', port='9999'):
    # database setup
    current = IOLoop.current()
    app = build_service(
        service_management={}
        )
    current.run_sync(
        lambda: db.init_app(app, **OWN_DB_INFO)
    )
    if SSL_DEPLOY:
        http_server = tornado.httpserver.HTTPServer(app, ssl_options=SSL_OPTIONS)
    else:
        http_server = tornado.httpserver.HTTPServer(app)
    # launch listener server
    http_server.listen(port)
    print(f'run service on port http://localhost:{port}')
    # launch services
    IOLoop.instance().start()


if __name__ == '__main__':
    launch_service()