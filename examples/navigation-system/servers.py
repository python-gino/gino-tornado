# -*- coding: utf-8 -*-
""" Web Application with tornado and gino.

endpoints:

- create dron, get dron info, edit dron info
- create route, get route info
- create point route, get points
"""

import json
from datetime import datetime
from tornado.web import Application, RequestHandler

from models import Dron, Route, RoutePoint


class DronHandler(RequestHandler):
    
    async def get(self, dronid):
        drone = await Dron.query.where(
            Dron.id == dronid
        ).gino.first()
        print('donhandler async get', drone)
        self.write({f'{dronid}': drone})

    async def post(self, dronid):
        data = json.loads(self.request.body)
        drone = Dron(**data)
        await drone.create()
        print('donhandler async post', drone)
        self.write({'created': drone.id})
        

class RouteHandler(RequestHandler):

    async def get(self, routeid):
        route = await Route.query.where(
            Route.id == routeid
        ).gino.first()
        print('routehandler async get', route)
        self.write({routeid: route})

    async def post(self, routeid):
        data = json.loads(self.request.body)
        dron = await Dron.query.where(
            Dron.id == data['dron_id']
        ).gino.first()
        print('routehandler async post dron', dron)
        if dron:
            data['start_timestamp'] = datetime.now()
            route = Route(**data)
            print(data, route)
            await route.create()
            print('routehandler async post route', route)
            self.write({'created': route.id})
        else:
            self.set_status(404, 'dron not created')


class RoutePointHandler(RequestHandler):

    async def post(self):
        data = json.loads(self.request.body)
        route = await Route.query.where(
            Route.id == data['route_id']
        ).gino.first()
        print('routepointhandler async post', route)
        if route:
            data['timestamp'] = datetime.now()
            routepoint = RoutePoint(**data)
            await routepoint.create()
            print('routepointhandler async post', routepoint)
            self.write({'created': routepoint.id})
        else:
            self.set_status(404, 'route not created')


def build_service(service_management=None):
    return Application([
        (r"/dron/([\w]*)", DronHandler),
        (r"/route/([\w]*)", RouteHandler),
        (r"/route-point/", RoutePointHandler),
    ], debug=True
    )