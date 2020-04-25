# -*- coding: utf-8 -*-
"""
Write tests with gino and tornado
"""
import os
from time import time, sleep
import json
import asyncio
from datetime import datetime, timedelta

from tornado.testing import unittest, AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from models import db
from settings import OWN_DB_INFO
from servers import build_service


class baseTestCase(AsyncHTTPTestCase):
    """Base class for tests"""

    def setUp(self):
        self.io_loop = IOLoop.current()
        # configure server and client
        super(AsyncHTTPTestCase, self).setUp()
        self.__port = self.get_http_port()
        self._app = self.get_app()
        # start gino app
        self.io_loop.run_sync(lambda: db.init_app(self._app, **OWN_DB_INFO))
        # define variables to launch tornado app
        self.http_server = self.get_http_server()
        self.http_server.listen(self.__port)
        self.http_client = AsyncHTTPClient()

    def tearDown(self):
        lp = asyncio.get_event_loop()
        # stop gino app
        lp.run_until_complete(self._app.db.pop_bind().close())
        # delete server and connections
        AsyncHTTPTestCase.tearDown(self)

    def get_app(self):
        """get application to launch server
        """
        app = build_service(
            service_management={}
        )
        return app

    def get_http_port(self):
        """get custom port to run server
        """
        return 9999

    def get_url(self, path):
        """customize url resolution on server, overridden
        because it was failing with localhost
        """
        port = self.get_http_port()
        return f'http://localhost:{port}{path}'


class missionTestCase(baseTestCase):
    
    def test_create_dron(self):
        # CREATE DRON
        raw = self.fetch('/dron/', method='POST', body=json.dumps(self.dron_info))
        created_dron = json.loads(raw)
        # CHECK RESPONSE 
        self.assertTrue('created' in created_dron)

    def test_create_route(self):
        # CREATE DRON
        # CREATE ROUTE
        # CHECK RESPONSE
        pass

    def test_add_routepoint(self):
        # CREATE DRON
        # CREATE ROUTE
        # ADD ROUTE POINT
        # CHECK RESPONSE
        pass

    def setUp(self):
        # define test infrastructure (app server, db connections)
        super().setUp()
        # create data for tests
        self.tmp_format = '%Y-%m-%d %H:%M:%S'
        now_time = datetime.now()
        self.dron_info = {
            'group': 'air_messager',
            'reference': 'xxxx'
        }
        self.route_info = {
            'initial_point': '0,0',
            'final_point':'100,100',
            'dron_id': '',
            'start_timestamp': now_time.strftime(self.tmp_format)
        }
        self.route_points_info = [
            {
                'route_id': f'{a}', 
                'timestamp': (now_time + timedelta(a)).strftime(self.tmp_format),
                'location_point': f'{a*10},{a*10}' 
                }
            for a in range(1, 10)
        ]

    def tearDown(self):
        # delete data
        # close connections and servers
        super().tearDown()
