# navigation system

simple tdd example to show basic gino use with tornado, how to build an application and how to test it.

to understand this example, read `tests.py` first, you will find how to start and stop a gino service and data associated with current example.

after that, you can read `models.py` where you can see how to define models in sqlalchemy fashion, and finally theck `servers.py` to check how gino and tornado work together as part of a backend application.

## setup envionment

this example was tested under Xubuntu 19.10, so, most of modern linux and macOS systems will perform in a similar way. to be able to run this example, you need to follow the steps bellow:

## dependencies

install postgres with `sudo apt-get install postgresql postgresql-contrib`, for postgresql configuration, you can check articles like [this one](https://tecadmin.net/install-postgresql-server-on-ubuntu/).

## python dependencies

install python [requirements](requirements.txt) with `pip install -r requirements.txt`

## setup database

connect to `myuser` user postgresql console by running `sudo -u myuser psql`, then, run in your psql console to create `ginotornadoex` database:

``` sql
create database ginotornadoex;

```

after that, create a secrets.json file with following information:

``` json
{
    "DATABASE_NAME": "ginotornadoex",
    "DATABASE_USER": "myuser",
    "DATABASE_HOST": "localhost",
    "DATABASE_PASS": "mypass"
  }
```

finally, to create tables inside database, run `python populate_db.py`

## run server and run tests

now, you can run tests with `python -m tornado.testing tests` that will use tornado.testing module to run all testcases in tests.py.

if you prefer run server and work with tools such as postman, you can run application with `python app.py `, it will start an app on localhost:9999, you can define your port with `--port` options, for instance, if you want to start server at port 9898, you must run `python app.py --port=9898`