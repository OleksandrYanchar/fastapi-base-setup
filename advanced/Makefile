NAMESPACE=fastapi-namespace

# Build and Deployment
kuber-build:
	./deploy.sh

# Delete Namespace and Volumes
kuber-delete:
	kubectl delete namespace $(NAMESPACE)

# PostgreSQL Commands
kuber-psql:
	kubectl exec -it $(POD_NAME_POSTGRES) -n $(NAMESPACE) -- psql -U fastapi -d postgres

# Backend Bash Access
.PHONY: backend-bash

kuber-bash:
	kubectl exec -it $(POD_NAME_BACKEND) -n $(NAMESPACE) -- bash


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
	docker exec -it fastapi-db psql -U fastapi -d postgres