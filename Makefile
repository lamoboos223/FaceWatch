.PHONY: run postgres clean-postgres restart-postgres setup install mongodb clean-mongodb restart-mongodb

# First-time setup (install deps + create db)
setup: install postgres

install:
	poetry install

# Run the Flask application
run:
	flask run --debug

# Create PostgreSQL database in Docker
postgres:
	docker run -d \
		--name facewatch-postgres \
		-e POSTGRES_DB=facewatch \
		-e POSTGRES_USER=facewatch \
		-e POSTGRES_PASSWORD=facewatch \
		-p 5432:5432 \
		postgres:15

# Stop and remove the database container
clean-postgres:
	docker stop facewatch-postgres || true
	docker rm facewatch-postgres || true

# Restart the database (useful for clean slate)
restart-postgres: clean-postgres postgres init-db

# Create MongoDB container
mongodb:
	docker run -d \
		--name facewatch-mongodb \
		-p 27017:27017 \
		-e MONGO_INITDB_ROOT_USERNAME=admin \
		-e MONGO_INITDB_ROOT_PASSWORD=password \
		mongo

# Stop and remove MongoDB container
clean-mongodb:
	docker stop facewatch-mongodb || true
	docker rm facewatch-mongodb || true

# Restart MongoDB (useful for clean slate)
restart-mongodb: clean-mongodb mongodb