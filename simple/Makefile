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
	sudo docker exec -it backend bash

clean:
	sudo docker-compose down -v

format:
	sudo docker exec -it backend isort app/
	sudo docker exec -it backend black app/
	sudo docker exec -it backend flake8 app/ 

create:
	python3 -m venv venv


req-d:
	pip install -r requirements/dev.txt


req-b:
	pip install -r requirements/base.txt

.PHONY: alembic-revision alembic-upgrade

alembic-revision:
	sudo docker exec -it backend alembic revision --autogenerate

alembic-upgrade:
	sudo docker exec -it backend alembic upgrade head

alembic-downgrade :
	sudo docker exec -it backend alembic downgrade base

psql:
	docker exec -it fastapi-db psql -U test -d postgres