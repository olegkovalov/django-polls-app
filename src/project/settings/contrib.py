import sys

import environ


env = environ.Env()


if 'test' in sys.argv:
    REDIS_DB = 3
    CELERY_ALWAYS_EAGER = True
else:
    # Redis
    REDIS_DB = env.int('REDIS_DB', default=2)
    REDIS_HOST = env.str('REDIS_HOST', default='localhost')

    # Celery
    CELERY_REDIS_DB = env.int('CELERY_REDIS_DB', default=2)
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL = 'redis://{host}/{redis_db}'.format(
        host=REDIS_HOST,
        redis_db=CELERY_REDIS_DB
    )
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = env.str('DJANGO_TIME_ZONE', default='UTC')
    CELERY_ALWAYS_EAGER = env.bool('CELERY_ALWAYS_EAGER', default=False)

REDIS_CONNECTION_STRING = env.str('REDIS_CONNECTION_STRING', default='redis://redis/{redis_db}').format(
    redis_db=REDIS_DB
)

# TODO
# SENDGRID_API_KEY = ''
