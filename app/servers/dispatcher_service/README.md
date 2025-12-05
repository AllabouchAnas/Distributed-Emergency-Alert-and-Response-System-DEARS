# Dispatcher Service

The **Dispatcher Service** is the central hub of the DEARS system. It receives emergency alerts from the web app and routes them to the correct response service (Police, Fire, or Medical) via RPC. This service is **stateless** and does not persist alerts to a database.

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.8+

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

# RPC Settings
RPC_RETRIES=2
RPC_TIMEOUT=5
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
  
- **Response:**
  ```json
  {
    "alert_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "forwarded",
    "timestamp": "2025-12-02T21:15:30.123456"
  }
  ```

**Note:** The `emergency_type` field is case-insensitive. You can send `"fire"`, `"FIRE"`, or `"Fire"` - all will be accepted and converted to uppercase.

### 2. Forwarding Alerts (Output)
The Dispatcher Service uses **RPC (Remote Procedure Calls)** to talk to the response services.

- **Police Service:** Connects to `localhost:9001`
- **Fire Service:** Connects to `localhost:9002`
- **Medical Service:** Connects to `localhost:9003`

When an alert comes in, the Dispatcher automatically calls the `receive_alert` function on the correct service.

### 3. Alert IDs
Alert IDs are generated as **UUIDs** (Universally Unique Identifiers) in string format. This ensures uniqueness without requiring a database.

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
