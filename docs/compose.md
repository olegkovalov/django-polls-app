Issues with Dockerfile / docker-compose
=======================================

* Containers with Django and Celery uses the same image. The difference is only in entry-points.
* `COPY . /polls` goes after `COPY requirements.txt /requirements.txt` and `RUN pip install -r /requirements.txt` to keep requirements installation before copying source files to effectively use caching in Docker images.
* Wait for migrations in Django / Celery entry-points.
* Use env files in `docker-compose.yml`.
* Use volumes in `docker-compose.yml`.
* Don't include Ansible to `requirements.txt` file.
