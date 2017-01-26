Run containers locally
======================

To run all containers locally you need to run command from repo root directory:

```
docker-compose --project-name polls up
```

or

```
make up
```

This commands will **download** required Docker images for Postgres, Redis, nginx, Django / Celery containers and run them.

Local image build VS downloading from hub
-----------------------------------------

If you're using `image` instruction in service definition inside `docker-compose.yml` image for Django / Celery will be downloaded from docker hub (or local machine). If you haven't pushed this image to hub yet it won't work.

Downloading ready image from hub:

```
app:
  image: doomatel/django-polls-webapp
  ...

celery:
  image: doomatel/django-polls-webapp
  ...
```

Instead of this you can build image locally and run all the containers. To do this you need to use `build` instructions for `app` and `celery` sections and volume `./src:/polls` in `docker-compose.yml`:

```
app:
  build:
    context: ./src
  ...
  volumes:
    - ./src:/polls
    - public_files:/polls/public
  ...  
celery:
  build:
    context: ./src
  ...
```

To rebuild containers after changes in Dockerfile you need to run:


```
docker-compose --project-name polls build
```

or

```
make build
```

Interaction with containers
---------------------------

You can check that the site is running by visiting [this page](http://127.0.0.1/). The only port is exposed is `80`.

If need direct access to any container to run some commands you can use [docker exec](https://docs.docker.com/engine/reference/commandline/exec/) command. For example let's create admin user in Django container:

```
docker exec -it polls_app_1 python manage.py createsuperuser
```

If you need to copy files from / to containers you can use [docker cp](https://docs.docker.com/engine/reference/commandline/cp/) command. Format of path arguments is similar to `scp`. For example lets copy DB dump from database container:

```
docker cp polls_database_1:/backups/dump.sql ./dump.sql
```

