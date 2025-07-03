ORo Robot Telemetry Dashboard
This project is a web-based telemetry dashboard for managing and monitoring ORo robot devices. It provides a RESTful API and WebSocket integration for real-time telemetry data, built with FastAPI, SQLAlchemy, PostgreSQL, and a simple HTML/JavaScript frontend.
Prerequisites
Ensure the following are installed:

Docker: Version 20.10 or higher
Docker Compose: Version 2.0 or higher
Python: Version 3.11 (optional for local development without Docker)
PostgreSQL Client: For database verification (e.g., psql)
Git: To clone the repository
VS Code (recommended) with WSL 2 integration for development on Windows

Project Structure
Ogmen-Assignment/
├── backend/
│   ├── crud.py
│   ├── database.py
│   ├── Dockerfile
│   ├── main.py
│   ├── migrations/
│   │   ├── env.py
│   │   ├── versions/
│   │   │   ├── initial_migration.py
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── ws_manager.py
├── frontend/
│   ├── app.js
│   ├── dashboard.html
│   ├── styles.css
├── docker-compose.yml
├── README.md

Setup Instructions

Clone the Repository
git clone https://github.com/Shivam-Gupta14/Ogmen-Assignment.git
cd Ogmen-Assignment


Verify Directory StructureEnsure all files are present:
ls
ls backend
ls backend/migrations
ls backend/migrations/versions
ls frontend

Expected output:
backend  docker-compose.yml  frontend  README.md
crud.py  database.py  Dockerfile  main.py  migrations  models.py  requirements.txt  schemas.py  ws_manager.py
env.py  versions
initial_migration.py
app.js  dashboard.html  styles.css


Update Imports (Fix ImportError)The main.py and crud.py files use absolute imports to align with the Docker volume mount. Verify:
cat backend/main.py
cat backend/crud.py

Ensure main.py has:
import models, schemas, crud, database, ws_manager

And crud.py has:
import models, schemas

If incorrect, update:
nano backend/main.py
nano backend/crud.py

Replace from . import ... with import ... as shown above.

Verify Dockerfile
cat backend/Dockerfile

Expected:
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

If incorrect, update:
nano backend/Dockerfile


Verify docker-compose.yml
cat docker-compose.yml

Expected:
name: assignmet
services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    depends_on:
      postgres:
        condition: service_started
    environment:
      - DATABASE_URL=postgresql://telemetry_user:password@postgres:5432/telemetry_db
    networks:
      - app-network
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./frontend:/app/frontend
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=telemetry_user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=telemetry_db
    networks:
      - app-network
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
networks:
  app-network:
    driver: bridge
volumes:
  postgres_data:

If incorrect, update:
nano docker-compose.yml



Migration Instructions

Build and Start Containers
docker-compose up --build

Wait for:

PostgreSQL: “database system is ready to accept connections”
Uvicorn: “Application startup complete”


Check Running Containers
docker ps

Expected:
CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS                    NAMES
<container_id> assignmet-api        "uvicorn main:app --…"   1 minute ago    Up 1 minute    0.0.0.0:8000->8000/tcp   assignmet_api_1
<container_id> postgres:15         "docker-entrypoint.s…"   1 minute ago    Up 1 minute    0.0.0.0:5433->5432/tcp   assignmet_postgres_1

Note the <api-container-name> (e.g., assignmet_api_1).

Apply MigrationsIn a new terminal:
cd /mnt/c/Users/Shivam/Desktop/Assignmet
docker ps
docker exec -it <api-container-name> alembic upgrade head

Expected:
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> <migration_id>, initial_migration


Verify Database Schema
psql -h localhost -U telemetry_user -d telemetry_db -W -p 5433 -c "\dt"

Enter password: passwordExpected:
List of relations
 Schema |     Name         | Type  |    Owner    
--------+------------------+-------+-------------
 public | command_logs     | table | telemetry_user
 public | robot_devices    | table | telemetry_user
 public | telemetry_data   | table | telemetry_user
 public | telemetry_metrics | table | telemetry_user



Run Instructions

Access the Application

Dashboard: Open http://localhost:8000/dashboard in a browser.
Select a device (after creating one via API).
View telemetry, summaries, and command logs.
Test commands (“Dispense Treat”, “Go to Location”).


API Documentation: Open http://localhost:8000/docs.
POST /devices/ (e.g., {"device_name": "Robot1", "model": "ORo1"}).
POST /metrics/{device_id}/data/ (e.g., {"metric_name": "battery_level", "value": "75"}).
GET /metrics/{device_id}/data/.
POST /commands/{device_id}/ (e.g., {"command": "dispense_treat"}).




Verify Data in Database
psql -h localhost -U telemetry_user -d telemetry_db -W -p 5433 -c "SELECT * FROM robot_devices;"
psql -h localhost -U telemetry_user -d telemetry_db -W -p 5433 -c "SELECT * FROM telemetry_metrics;"


Stop Containers
docker-compose down



Troubleshooting

ImportError: attempted relative import with no known parent package

Ensure main.py and crud.py use absolute imports (import models, schemas).

Check container files:
docker run -it assignmet-api ls /app

Expected: crud.py database.py main.py migrations models.py requirements.txt schemas.py ws_manager.py



Docker Compose Errors

Check logs:
docker logs assignmet_api_1
docker logs assignmet_postgres_1




Port Conflicts

Check and resolve:
sudo lsof -i :5433
sudo lsof -i :8000
sudo kill <pid>




Frontend Issues

Verify frontend files:
cat frontend/app.js
cat frontend/styles.css


Test: http://localhost:8000/static/app.js


Contributing

Fork the repository.
Create a feature branch: git checkout -b feature-name
Commit changes: git commit -m "Add feature-name"
Push to the branch: git push origin feature-name
Create a pull request.

Contact
For issues or contributions, contact Shivam Gupta via GitHub: Shivam-Gupta14 or LinkedIn www.linkedin.com/in/shivam-gupta-582221291
