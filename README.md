Django polls app wrapped in Docker containers
=============================================

This is an [example](https://docs.djangoproject.com/en/dev/intro/tutorial01/) Django application wrapped in Docker containers:

* Django application (custom image based [python:3.5.2-alpine](https://hub.docker.com/_/python/)).
* Celery (same image as for Django but with different entrypoint).
* Postgres (official [postgres:9.5-alpine](https://hub.docker.com/_/postgres/)).
* Redis (official [redis:3.2-alpine](https://hub.docker.com/_/redis/)).
* Nginx (official [nginx:mainline-alpine](https://hub.docker.com/_/nginx/)).

This example is made to learn how to wrap Django projects in Docker.

The original code of application was taken from [here](https://github.com/Chive/django-poll-app).

Important information
---------------------

If you'll fork this repo the first thing you should do is to change docker image in `docker-compose.yml` for `app` and `celery` services:

```
app:
  image: doomatel/django-polls-webapp
  ...
celery:
  image: doomatel/django-polls-webapp
  ...
```

Use your own account / image on [Docker Hub](https://hub.docker.com/).

Documentation
-------------

* [Checklist for wrapping your project into containers](docs/checklist.md).
* [Run services for local development](src/README.md).
* [Compose issues](docs/compose.md).
* [Run all containers locally](docs/run_locally.md).
* [CI configuration](docs/ci_config.md).
* [Deployment with Ansible](docs/ansible.md).

Vagrant
-------

```
vagrant up
```

Wait for its provision is ready and go to [this page](127.0.0.1:8080).

TODO
----

* Cover code with more tests.
* Add sendgrid.
