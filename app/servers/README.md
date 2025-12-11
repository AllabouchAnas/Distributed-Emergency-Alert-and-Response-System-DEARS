# Distributed Emergency Alert and Response System (DEARS)

This directory contains all microservices of the DEARS backend:
- **Dispatcher Service**: Central hub, receives/forwards alerts.
- **Response Services**: Police, Fire, and Medical emergency handling.

## 🛠️ Prerequisites
- **Python** 3.8+
- **PostgreSQL** server running locally (see each service's docs for env settings)

---

## 🚀 Setup (All Platforms)

**1. Clone and move to this directory:**
```bash
cd app/servers
```

**2. Create a virtual environment and install requirements:**
- **Linux/macOS:**
    ```bash
    ./setup_env.sh
    ```
- **Windows (cmd/powershell):**
    ```bat
    setup_env.bat
    ```

**3. Create your `.env` files** for each service.
- Copy `.env.example` (if present) to `.env` inside each service directory (see dispatcher and police_service for sample formats). Adjust DB connection and service ports as needed.

---

## ▶️ Running All Services Automatically

### **Linux/Mac (or WSL)**
```bash
./start_all.sh
```

### **Windows**
Double-click `start_all.bat` or run:
```bat
start_all.bat
```
This launches every microservice in its own console window.

- These scripts run `run_all_services.py`, which starts each Python service in the right way for your OS.

---

## ▶️ Running Services Manually
For development, you might want to run one or more services directly.

**Dispatcher**
```bash
cd dispatcher_service
python run.py
```

**Police, Fire, or Medical Service**
```bash
cd response_services/<service_name>
python run.py
```
Replace `<service_name>` with `police_service`, `fire_service`, or `medical_service`.

- Each `run.py` sets up Python paths so you can start individual services easily.

---

## 📝 Service-Specific Configuration
See:
- `dispatcher_service/README.md` for endpoints/configuration
- `response_services/police_service/README.md` for police config

All services require proper environment variables (`.env`) and a running PostgreSQL DB.

---

## 🔄 Stopping the Services
- **If you used `start_all.bat` or `start_all.sh`**, just close the opened windows or press `Ctrl+C` in the main terminal to stop everything.

---

## 🧪 Testing Locally
- Look in the dispatcher and service subdirs for included test scripts (see their READMEs).

---

## ❓ Troubleshooting
- Make sure your Python virtualenv is activated before installing or running services.
- For Linux/macOS use: `./setup_env.sh`.
- For Windows use: `setup_env.bat` (do not run venv/pip manually).
- If `./setup_env.sh` fails, check that `python3` is installed and available in PATH.
- For Windows, prefer using PowerShell or CMD (not Git Bash).
- Ensure `.env` files have correct DB connection info for each service.

---

## License
MIT
