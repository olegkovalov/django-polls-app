.PHONY: up

up:
	docker-compose --project-name polls up

build:
	docker-compose --project-name polls build

deploy:
	ansible-playbook provisioning/server.yml -l prod -e env=prod -i provisioning/inventory/prod

sinclude makefile-local
