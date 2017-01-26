Checklist for wrapping into containers
--------------------------------------

The most easiest way is to follow [12 Factor](http://12factor.net/) methodology. Some of its statements are covered by Python best practices such as keeping 3rd-party requirements outside of main repo in virtual environment. Some statements are covered by Django itself. But there are several statements we need to change some parts of standard Django project.

Settings in environment
-----------------------

The main idea is to keep settings in [environment variables](https://en.wikipedia.org/wiki/Environment_variable). `settings.py` file in Django project is code like models or views. It isn't just a key / value configuration file. This is an advantage and disadvantage at the same time. To keep persistence between different environments (local / dev / stage / production) we need only one settings file. And the setting should be key / value pair in environment variables or plain configuration files.

The best solution is [django-environ](https://github.com/joke2k/django-environ). It allows to reads settings from environment or text file. Settings that were set directly have bigger priority then settings from file.

For example let's change the database for running a shell:

```
DATABASE_URL=psql://192.168.59.103:5432/foobar_db ./manage.py shell
```

`django-environ` can work with different [Python types](https://github.com/joke2k/django-environ#supported-types) such as string, integers, booleans, lists, dictionaries, etc.

Separate files for Django, 3rd parties and project settings
-----------------------------------------------------------

This isn't a strong best practice but we've found it very useful. The main benefit of using three (actually four including `_django_apps.py` file) is that you can easily find required setting definition. According to filenames setting files keep settings for:

* `django.py` - Django related settings.
* `contrib.py` - settings for 3rd-party requirements like Django REST Framework, Celery, etc.
* `project.py` - settings created by developers in project applications.
* `_django_apps.py` - `INSTALLED_APPS` setting splitted into three parts: `DJANGO_APPS`, `CONTRIB_APPS` and `PROJECT_APPS`.

There are some edge cases when you can't explicitly define which file you should use. For example: We use `django-debug-toolbar` for local development (only when `DEBUG` setting is True). It requires to add middleware. So we can add following code to `settings/django.py` file:

```
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
```

At the first time it's a controversial decision because `INSTALLED_APPS` and `MIDDLEWARE_CLASSES` are the Django settings, while `INTERNAL_IPS` is from django-debug-toolbar, which is a third-party application and should keep its configuration in `settings/contrib.py`. In this case we can add an exception: *if 3rd party app requires changes in Django settings this code should be placed in `settings/django.py` and not in `settings/contrib.py`*

By the way we don't have any issues with accessing to settings from another "files" because we have all settings in environment variables and we can access to them anywhere we want.

Settings for different environments
-----------------------------------

`django-environ` allows us to keep settings in text files and read them on startup. By default it's file `.env` from the current directory. Usually this file is ignored by git. We can create separate file for each environment we need (`.env.dev`, `.env.stage`, `.env.prod`, etc) and make symlinks to `.env` file. Also it's very good to have default settings for local development in `.env.example`.
