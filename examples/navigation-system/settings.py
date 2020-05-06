# -*- coding: utf-8 -*-
import os
import json


SECRETS = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'secrets.json'
    )

with open(SECRETS, 'r') as f:
    raw = json.loads(f.read().strip())

DB_INFO = {
    'host': raw["DATABASE_HOST"],
    'port': 5432,
    'dbname': raw["DATABASE_NAME"],
    'user': raw["DATABASE_USER"],
    'password': raw["DATABASE_PASS"],
}

# SETTINGS FOR GINO DATABASE SERVICE
OWN_DB_INFO = {
    'host': raw["DATABASE_HOST"],     # database host
    'port': 5432,                     # database port, 5432 is postgresql default
    'database': raw["DATABASE_NAME"], # database name
    'user': raw["DATABASE_USER"],     # database user, owner of database
    'password': raw["DATABASE_PASS"], # database password
    'ssl': False,                     # if your database hosts is an https server, set this True
    'pool_min_size': 2,               # min amount of gino connections to database
    'pool_max_size': 5                # max amount of gino connections to database
}