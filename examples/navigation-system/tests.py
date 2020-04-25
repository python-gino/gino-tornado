# -*- coding: utf-8 -*-
"""
Write tests with gino and tornado
"""
import os
from time import time, sleep
import json
import asyncio
from datetime import datetime

from tornado.testing import unittest, AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from models import db
from settings import OWN_DB_INFO
from servers import build_service


class baseTestcase(AsyncHTTPTestCase):
    """Base class for tests"""

    def setUp(self):
        self.io_loop = IOLoop.current()
        # configure server and client
        super(AsyncHTTPTestCase, self).setUp()
        self.__port = self.get_http_port()
        self._app = self.get_app()
        self.io_loop.run_sync(lambda: db.init_app(self._app, **OWN_DB_INFO))
        self.http_server = self.get_http_server()
        self.http_server.listen(self.__port)
        self.http_client = AsyncHTTPClient()
        lp = asyncio.get_event_loop()

    def tearDown(self):
        print('=/c-'*100)
        # delete data and accounts created, can be disabled putting del False at self.st
        lp = asyncio.get_event_loop()
        # stop gino
        lp.run_until_complete(self._app.db.pop_bind().close())
        # delete server and connections
        AsyncHTTPTestCase.tearDown(self)

    def get_app(self):
        """get application to launch server
        """
        app = build_service(
            service_management={}
        )
        # self.io_loop.run_sync(lambda: db.init_app(app, **OWN_DB_INFO))
        return app

    def get_http_port(self):
        """get custom port to run server
        """
        return 9009

    def get_url(self, path):
        """customize url resolution on server, overridden
        because it was failing with localhost
        """
        port = self.get_http_port()
        return f'http://localhost:{port}{path}'