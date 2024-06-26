up-build:
	sudo docker-compose build
	sudo docker-compose up

build:
	sudo docker-compose build


down:
	sudo docker-compose down


up-d:
	sudo docker-compose up -d

up:
	sudo docker-compose up

stop:
	sudo docker-compose down


bash:
	sudo docker exec -it auto-backend bash

clean:
	sudo docker-compose down -v

format:
	black app/ 

create:
	python3 -m venv venv


req-d:
	pip install -r requirements/dev.txt


req-b:
	pip install -r requirements/base.txt

.PHONY: alembic-revision alembic-upgrade

alembic-revision:
	sudo docker exec -it auto-backend alembic revision --autogenerate

alembic-upgrade:
	sudo docker exec -it auto-backend alembic upgrade head

alembic-downgrade :
	sudo docker exec -it auto-backend alembic downgrade base

psql:
	docker exec -it fastapi-db psql -U test -d postgres
