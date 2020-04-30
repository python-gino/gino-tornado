# -*- coding: utf-8 -*-
"""
Write tests with gino and tornado.
"""
import json
import asyncio
from datetime import datetime, timedelta

from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from models import db, Dron, Route, RoutePoint
from settings import OWN_DB_INFO
from servers import build_service


class baseTestCase(AsyncHTTPTestCase):
    """Base class for tests."""

    def setUp(self):
        self.io_loop = IOLoop.current()
        # CONFIGURE TORNADO SERVER AND CLIENT
        super().setUp()
        self.__port = self.get_http_port()
        self._app = self.get_app()
        self.http_client = AsyncHTTPClient()
        # START GINO APP
        # start gino core service as defined at models.py
        self.io_loop.run_sync(lambda: db.init_app(self._app, **OWN_DB_INFO))
        # SETUP TORNADO APP SERVER
        self.http_server = self.get_http_server()
        self.http_server.listen(self.__port)

    def tearDown(self):
        lp = asyncio.get_event_loop()
        # STOP GINO APP
        # stop gino app to release db connections
        # excecutors and file descriptors
        lp.run_until_complete(self._app.db.pop_bind().close())
        # delete server and connections
        AsyncHTTPTestCase.tearDown(self)

    def get_app(self):
        """Get application to launch server.
        """
        app = build_service(
            service_management={}
        )
        return app

    def get_http_port(self):
        """Get custom port to run server.
        """
        return 9999

    def get_url(self, path):
        """Gustomize url resolution on server, overridden
        because it was failing with localhost.
        """
        port = self.get_http_port()
        return f'http://localhost:{port}{path}'


class missionTestCase(baseTestCase):
    """Test endpoints of web application.
    """

    def test_create_dron(self):
        # CREATE DRON
        raw = self.fetch('/dron/', method='POST', body=json.dumps(self.dron_info))
        created_dron = json.loads(raw.body)
        # CHECK RESPONSE
        self.assertTrue('created' in created_dron)

    def test_create_route(self):
        # CREATE DRON
        raw = self.fetch('/dron/', method='POST', body=json.dumps(self.dron_info))
        created_dron = json.loads(raw.body)
        self.assertTrue('created' in created_dron)
        # CREATE ROUTE
        self.route_info['dron_id'] = created_dron['created']
        raw = self.fetch('/route/', method='POST', body=json.dumps(self.route_info))
        created_route = json.loads(raw.body)
        # CHECK RESPONSE
        self.assertTrue('created' in created_route)

    def test_add_routepoint(self):
        # CREATE DRON
        raw = self.fetch('/dron/', method='POST', body=json.dumps(self.dron_info))
        created_dron = json.loads(raw.body)
        # CREATE ROUTE
        self.route_info['dron_id'] = created_dron['created']
        raw = self.fetch('/route/', method='POST', body=json.dumps(self.route_info))
        created_route = json.loads(raw.body)
        self.assertTrue('created' in created_route)
        # ADD ROUTE POINT
        for item in self.route_points_info:
            item['route_id'] = created_route['created']
        for point in self.route_points_info:
            raw = self.fetch('/route-point/', method='POST', body=json.dumps(point))
            created_point = json.loads(raw.body)
            # CHECK RESPONSE
            self.assertTrue('created' in created_point)

    def setUp(self):
        # define data for testing
        # this app was built to track missions of drone fleets
        super().setUp()
        # create data for tests
        self.tmp_format = '%Y-%m-%d %H:%M:%S'
        now_time = datetime.now()
        self.dron_info = {
            'group': 'air_messager', # fleet name
            'reference': 'xxxx'      # drone id
        }
        self.route_info = {
            'initial_point': '0,0',  # coordinates of initial point
            'final_point':'100,100', # coordinates of final point
            'dron_id': '',           # dron allocated
            'start_timestamp': now_time.strftime(self.tmp_format)
        }
        self.route_points_info = [
            {
                'route_id': f'{a}',                    # route being tracked
                'location_point': f'{a*10},{a*10}' ,   # current location point
                'timestamp': (now_time + timedelta(a)).strftime(self.tmp_format),
                }
            for a in range(1, 10)
        ]

    def tearDown(self):
        lp = asyncio.get_event_loop()
        # delete data created during tests
        lp.run_until_complete(
            RoutePoint.delete.gino.all()
            )
        lp.run_until_complete(
            Route.delete.gino.all()
            )
        lp.run_until_complete(
            Dron.delete.gino.all()
            )
        # close connections and servers
        super().tearDown()
