# Cone search API

This is a tiny FastAPI project that defines a possible future IVOA simple
cone search API. It does not implement cone search, only provides an API
stub from which FastAPI can generate an OpenAPI spec and generate
interactive documentation pages.

The API here was based on [Simple Cone Search 1.03](https://www.ivoa.net/documents/REC/DAL/ConeSearch-20080222.html).

This is part of the work of the Protocol Transition Tiger Team.

## Prerequisites

* Python 3.11 or later.

If you do not have Python available, you can still use the pre-generated
OpenAPI schema found in `openapi.json`.

## Setup

To use this repository, start by creating a Python [virtual
environment](https://docs.python.org/3/library/venv.html) through any
method of your choice. Activate that environment. Then, run the following
command to install dependencies and the cone-search code:

    pip install -e .

## Start the application

To start the example application, run:

    cone-search run
    
This will start a FastAPI application listening on localhost, port 8080 by
default. You can change the port with the `--port` flag. You can now view
the rendered documentation for the API at either:

    http://localhost:8080/cone-search/docs
    http://localhost:8080/cone-search/redoc
    
The first uses [Swagger](https://swagger.io/tools/swagger-ui/) and the
second uses [Redoc](https://github.com/Redocly/redoc).

## Generate the OpenAPI schema

A pregenerated version of the OpenAPI schema has been committed to the
repository as `openapi.json` for convenience. If you want to regenerate it
(after making changes, for example), run:

    cone-search openapi-schema -o openapi.json
