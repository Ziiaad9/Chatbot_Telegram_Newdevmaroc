.PHONY: run dev init-db test docker-build docker-run docker-up docker-down

run:
	python app/main.py

init-db:
	python migrations/init_db.py

test:
	pytest -v

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Afficher les logs
logs:
	docker-compose logs -f bot
