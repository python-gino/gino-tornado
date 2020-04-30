# -*- coding: utf-8 -*-
""" Databases models and storages.
"""
from gino_tornado import Gino

# DEFINE GINO CORE
# gino extension for tornado is an object that
# allow user start/stop gino service as an
# application used as parent class of models or
# inside tornado request handlers, this example
# uses gino as parent class for models
db = Gino()


class Dron(db.Model):
    """Define dron information.
    """
    __tablename__ = 'drones'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    group = db.Column(db.String(30))
    reference = db.Column(db.String(30))

    def dict_repr(self):
        return {
            'id': str(self.id),
            'group': self.group,
            'reference': self.reference
        }


class Route(db.Model):
    """Define a route for dron to run.
    """
    __tablename__ = 'routes'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    initial_point = db.Column(db.String(30))
    final_point = db.Column(db.String(30))
    dron_id = db.Column(db.Integer())
    start_timestamp = db.Column(db.DateTime())

    def dict_repr(self):
        return {
            'id': str(self.id),
            'initial_point': self.initial_point,
            'final_point': self.final_point,
            'dron_id': self.dron_id,
            'start_timestamp': self.start_timestamp
        }

    async def traceback(self):
        points = await RoutePoint.query.where(
            RoutePoint.route_id == str(self.id)
        ).gino.first()
        return [a.dict_repr() for a in points]


class RoutePoint(db.Model):
    """Define an ownCloud user.
    """
    __tablename__ = 'routepoints'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer())
    timestamp = db.Column(db.DateTime())
    location_point = db.Column(db.String(30), unique=True)

    def dict_repr(self):
        return {
            'id': str(self.id),
            'route_id': self.route_id,
            'timestamp': self.timestamp,
            'location_point': self.location_point
        }
