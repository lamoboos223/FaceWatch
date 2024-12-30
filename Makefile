.PHONY: run db init-db clean-db restart-db setup install

# First-time setup (install deps + create db + init tables)
setup: install db init-db

install:
	poetry install

# Run the Flask application
run:
	flask run --debug

# Create PostgreSQL database in Docker
db:
	docker run -d \
		--name face-recognition-db \
		-e POSTGRES_DB=facewatch \
		-e POSTGRES_USER=facewatch \
		-e POSTGRES_PASSWORD=facewatch \
		-p 5432:5432 \
		postgres:15

# Initialize the database tables
init-db:
	python init_db.py

# Stop and remove the database container
clean-db:
	docker stop face-recognition-db || true
	docker rm face-recognition-db || true

# Restart the database (useful for clean slate)
restart-db: clean-db db init-db