# -*- coding: utf-8 -*-
import os
import json
import queries

from models import db


def launch_migration():
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
    db_endpoint = queries.uri(**DB_INFO)
    print('connection string')
    import sqlalchemy as sa
    print('doing engine')
    db_engine = sa.create_engine(db_endpoint)
    print('creating stuff')
    db.create_all(bind=db_engine)
    print('stoping stuff')
    db_engine.dispose()
    print('done')


if __name__ == '__main__':
    launch_migration()