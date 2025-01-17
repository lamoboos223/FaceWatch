# Facewatch

A facial recognition-based watchlist system that allows you to register faces and verify them against a database.

## Features

- Face Registration: Upload images with associated URLs and reasons
- Face Verification: Check if a face exists in the watchlist
- PostgreSQL Database: Secure storage of face data
- Real-time Face Recognition: Using face_recognition library

## Prerequisites

- Python 3.10 or higher
- Poetry (Python package manager)
- Docker
- Make
- CMake (for dlib compilation)

  ```bash
  # Windows (using chocolatey)
  choco install cmake
  
  # macOS
  brew install cmake
  
  # Ubuntu/Debian
  sudo apt-get install cmake
  ```

## Quick Start

1. Setup the project:

   ```bash
   make setup
   ```

2. Run the application:

   ```bash
   make run
   ```

   The application will be available at <http://localhost:5000>

## Development Commands

| Command | Description |
|---------|-------------|
| `make setup` | First-time setup (install deps + create db + init tables) |
| `make run` | Start the Flask application |
| `make db` | Create PostgreSQL database in Docker |
| `make init-db` | Initialize database tables |
| `make clean-db` | Stop and remove database container |
| `make restart-db` | Reset database (clean slate) |
| `make mongodb` | Create MongoDB container |
| `make clean-mongodb` | Stop and remove MongoDB container |
| `make restart-mongodb` | Reset MongoDB (clean slate) |

---

```mermaid
classDiagram
    class DatabaseInterface {
        +connect()
        +query()
    }
    
    class PostgreSQLDB {
        +connect()
        +query()
    }
    
    class MongoDB {
        +connect()
        +query()
    }
    
    class DBFactory {
        +get_db()
    }
    
    class Config {
        +DB_TYPE: string
    }
    
    DatabaseInterface <|-- PostgreSQLDB
    DatabaseInterface <|-- MongoDB
    DBFactory ..> PostgreSQLDB : creates
    DBFactory ..> MongoDB : creates
    DBFactory --> Config : reads
```

---

```mermaid
sequenceDiagram
    participant App
    participant Config
    participant Factory as get_db()
    participant PostgreSQL
    participant MongoDB
    
    App->>Config: Read DB_TYPE
    Config-->>Factory: Return "postgresql" or "mongodb"
    
    alt DB_TYPE is "postgresql"
        Factory->>PostgreSQL: Create instance
        PostgreSQL-->>App: Return PostgreSQL connection
    else DB_TYPE is "mongodb"
        Factory->>MongoDB: Create instance
        MongoDB-->>App: Return MongoDB connection
    end
```

---

```mermaid
graph LR
    A[Application] --> B[get_db Factory]
    C[Configuration] --> B
    B --> D[PostgreSQL]
    B --> E[MongoDB]
```

---

```mermaid
sequenceDiagram
    App->>Config: Get DB_TYPE
    Config->>Factory: Return setting
    Factory->>Database: Create instance
    Database->>App: Return connection
```

---

```mermaid
graph TD
    A[Your Code] -->|calls| B[Abstraction Layer add/commit]
    B -->|if postgresql| C[SQLAlchemy add/commit]
    B -->|if mongodb| D[MongoDB insert/save]
```
