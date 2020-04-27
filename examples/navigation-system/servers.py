"""
endpoints:

- create dron, get dron info, edit dron info
- create route, get route info
- create point route, get points
"""
import asyncio
import json
from tornado.web import Application, RequestHandler

from models import Dron, Route, RoutePoint


class DronHandler(RequestHandler):
    
    async def get(self, dronid):
        drone = await Dron.query.where(
            Dron.id == dronid
        ).gino.first()
        self.write({f'{dronid}': drone})

    async def post(self, dronid):
        data = json.loads(self.request.body)
        drone = Dron(**data)
        await drone.create()
        self.write({'created': drone.id})
        

class RouteHandler(RequestHandler):
    
    async def get(self, routeid):
        route = await Route.query.where(
            Route.id == routeid
        ).gino.first()
        self.write({routeid: route})

    async def post(self, routeid):
        route = await Route.query.where(
            Route.id == routeid
        ).gino.first()
        if route:
            data = json.loads(self.request.body)
            route = Route(**data)
            await route.create()
            self.write({'created': route.id})
        else:
            self.set_status(404, 'dron not created')  


class RoutePointHandler(RequestHandler):

    async def post(self):
        data = json.loads(self.request.body)
        route = await Route.query.where(
            Route.id == data['route_id']
        ).gino.first()
        if route:
            routepoint = RoutePoint(**data)
            await routepoint.create()
            self.write({'created': routepoint.id})
        else:
            self.set_status(404, 'route not created')


def build_service(service_management=None):
    return Application([
        (r"/dron/([\w]*)", DronHandler, {'service_management': service_management}),
        (r"/route/([\w]*)", RouteHandler, {'service_management': service_management}),
        (r"/route-point/", RoutePointHandler, {'service_management': service_management}),
    ], debug=True
    )