.PHONY: run

run:
	python manage.py runserver 0.0.0.0:8000

clean_pyc:
	find . -name \*.pyc -delete
	find . -name \*.pyo -delete

celery:
	celery -A project worker -l DEBUG

dev_docker:
	docker-compose --project-name polls --file docker-compose-development.yml up

test:
	./manage.py test --testrunner=django_nose.NoseTestSuiteRunner -v 2 --parallel

test_with_coverage:
	coverage run ./manage.py && ./manage.py test --testrunner=django_nose.NoseTestSuiteRunner --noinput --with-coverage --cover-package=api --cover-html

sinclude makefile-local
