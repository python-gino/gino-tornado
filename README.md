# gino-tornado

An extension for GINO to support Tornado server.

## Contents

- examples
- [navigation system](examples/navigation-system/index.md): simple tdd crud app for drone route management, contains a simple tornado-gino application and its tornado.testing testcases.
- tutorials
- basic tornado-gino (soon)
- production tips (soon)

## Current status

Since GINO 1.0, the built-in extensions are now separate projects supported by
the community. This project is copied here directly from GINO 0.8.x for
compatibility. 

In the `models.py` file at `navigation-system` example you can find a guide to 
make migration to GINO 1.0, that example also contain tests of extension for
Tornado 6.0.4 and GINO 1.0 that works on Xubuntu 19.10, current goal lays on
extend those tests and add production-ready features.

Help is needed to:

* Keep this project maintained - follow Tornado releases, fix issues, etc.
* Add more examples and documentation.
* Answer questions in the community.
