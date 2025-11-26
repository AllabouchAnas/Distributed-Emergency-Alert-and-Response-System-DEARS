# Dispatcher Service

The **Dispatcher Service** is the central hub of the DEARS system. It receives emergency alerts from the web app and routes them to the correct response service (Police, Fire, or Medical).

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.8+
- PostgreSQL (running locally)

### 2. Installation
```bash
# Clone and enter directory
cd dispatcher_service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file (copy from `.env.example`):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dears_db

# Server Settings
DISPATCHER_HOST=0.0.0.0
DISPATCHER_PORT=8000

# RPC Services (Where to send alerts)
RPC_POLICE_HOST=localhost
RPC_POLICE_PORT=9001
RPC_FIRE_HOST=localhost
RPC_FIRE_PORT=9002
RPC_MEDICAL_HOST=localhost
RPC_MEDICAL_PORT=9003
```

### 4. Run the Service
```bash
python run.py
```
The service will start at `http://localhost:8000`.

---

## 🔗 How It Connects

### 1. Receiving Alerts (Input)
The **Django Web App** sends alerts here via HTTP POST.

- **Endpoint:** `POST /submit-alert`
- **URL:** `http://localhost:8000/submit-alert`
- **Payload:**
  ```json
  {
    "user_id": 1,
    "description": "Fire in the kitchen",
    "location": "123 Main St",
    "emergency_type": "FIRE"
  }
  ```

### 2. Forwarding Alerts (Output)
The Dispatcher Service uses **RPC (Remote Procedure Calls)** to talk to the response services.

- **Police Service:** Connects to `localhost:9001`
- **Fire Service:** Connects to `localhost:9002`
- **Medical Service:** Connects to `localhost:9003`

When an alert comes in, the Dispatcher automatically calls the `receive_alert` function on the correct service.

### 3. Database
All alerts are saved to the **PostgreSQL** database before being forwarded.

---

## 🧪 Testing Locally

We have included test scripts to help you verify everything is working.

1. **Start the Dispatcher:** `python run.py`
2. **Start Mock Services:** (Open new terminals for each)
   - `python test_mock_police_service.py`
   - `python test_mock_fire_service.py`
   - `python test_mock_medical_service.py`
3. **Run Test Client:**
   - `python test_http_client.py --auto`

This will simulate the full flow: Web App -> Dispatcher -> Response Service.
