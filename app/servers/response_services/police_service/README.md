# Police Service

This service handles emergency alerts of type "POLICE". It is an RPyC server that receives alerts from the Dispatcher, finds the nearest available police unit, and dispatches it.

## Setup

1.  **Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Update `DATABASE_URL` in `.env` to point to your PostgreSQL database.
    - Ensure `POLICE_SERVICE_PORT` matches the dispatcher's configuration (default: 9001).

## Running the Service

Run the service as a module from the project root:

```bash
python -m app.servers.response_services.police_service.main
```

## Verification

Run the verification script to test the service (ensure service is running first):

```bash
python app/servers/response_services/police_service/verify_service.py
```
