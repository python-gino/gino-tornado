# -*- coding: utf-8 -*-
"""
Databases models and storages
"""
from datetime import datetime
from gino.ext.tornado import Gino


db = Gino()


class Dron(db.Model):
    """Define dron information
    """
    __tablename__ = 'drones'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    group = db.Column(db.String(30), unique=True)
    timestamp = db.Column(db.String(30), default='None')


class Route(db.Model):
    """Define a route for dron to run
    """
    __tablename__ = 'routes'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    initial_point = db.Column(db.String(30), unique=True)
    final_point = db.Column(db.String(30), unique=True)
    dron_id = db.Column(db.Integer())
    start_timestamp = db.Column(db.DateTime())


class RoutePoint(db.Model):
    """Define an ownCloud user.
    """
    __tablename__ = 'routepoints'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer())
    timestamp = db.Column(db.DateTime())
    location_point = db.Column(db.String(30), unique=True)

