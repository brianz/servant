# Servant

[![Build Status](https://travis-ci.org/clearcare/servant.svg?branch=master)](https://travis-ci.org/clearcare/servant)

A python package to build services/microservices.

http://blog.brianz.bz/post/introducting-servant/

What exactly is this library? At a very high level servant is:

- a Python library/framework for authoring and communicating with services
- to services what Django/Flask/Rails are to web applications
- designed primarily for internal non-publicly facing services

Servant is actually pretty simple and doesn’t perform much magic. What it does do is give you, the service author, a
framework for designing RPC-style services in Python which can run on their own, independently, and are easy to connect to
and interface with. In addition, it’s not an opinionated framework so you can choose whatever tooling you’d like in order to
author your service. A typical recipe may include:

- pytest for testing 
- sqlalchemy for talking to the Postgres.

However, you use whatever you want depending on your needs. Servant stays out of your way and deals with executing service
calls on behalf of the client.

See the `examples` folder to see what a service server and client look like.

Servant is currently being used in production at [Clearcare](http://clearcareonline.com) and as such, is supported well.
