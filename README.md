ORo Robot Telemetry Dashboard
A real-time telemetry dashboard for managing and monitoring ORo robot devices. Built with FastAPI, PostgreSQL, Docker, and a simple HTML/JS frontend.
🧰 Prerequisites
Docker v20.10+
Docker Compose v2.0+
Python 3.11 (optional for local development)
PostgreSQL Client (psql)
Git
VS Code + WSL 2 (recommended on Windows)

📁 Project Structure
pgsql
Copy
Edit
Ogmen-Assignment/
├── backend/
│   ├── main.py, crud.py, database.py, models.py, schemas.py, ws_manager.py
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/
│   │       └── initial_migration.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.js, dashboard.html, styles.css
├── docker-compose.yml
└── README.md
🚀 Getting Started
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/Shivam-Gupta14/Ogmen-Assignment.git
cd Ogmen-Assignment


3. Build & Run the App
bash
Copy
Edit
docker-compose up --build
Wait for logs:

Uvicorn running...

PostgreSQL: ready to accept connections

📦 Database Migrations
Apply Migrations
bash
Copy
Edit
docker ps  # get API container name
docker exec -it <api-container-name> alembic upgrade head
Verify Tables
bash
Copy
Edit
psql -h localhost -U telemetry_user -d telemetry_db -W -p 5433 -c "\dt"
🌐 Access the App
Dashboard: http://localhost:8000/dashboard

API Docs: http://localhost:8000/docs

🔧 API Examples
Create Device
json
Copy
Edit
POST /devices/
{
  "device_name": "Robot1",
  "model": "ORo1"
}
Push Metric
json
Copy
Edit
POST /metrics/{device_id}/data/
{
  "metric_name": "battery_level",
  "value": "75"
}
Fetch Data
http
Copy
Edit
GET /metrics/{device_id}/data/
Send Command
json
Copy
Edit
POST /commands/{device_id}/
{
  "command": "dispense_treat"
}
🛑 Stop Containers
bash
Copy
Edit
docker-compose down
🛠️ Troubleshooting
Port Conflicts
bash
Copy
Edit
sudo lsof -i :8000
sudo kill <PID>
Alembic Import Errors
Ensure main.py and crud.py use:

python
Copy
Edit
import models, schemas
Logs
bash
Copy
Edit
docker logs assignmet-api-1
docker logs assignmet-postgres-1
🤝 Contributing
Fork this repo

Create your branch git checkout -b feature-name

Commit & push

Open a pull request

📫 Contact
Shivam Gupta

GitHub: Shivam-Gupta14

LinkedIn: linkedin.com/in/shivam-gupta-582221291
