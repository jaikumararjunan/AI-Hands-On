# v1.4 Application UI Fix

The Docker bundle now exposes two separate browser experiences:

- **Application UI** — customer-facing commerce storefront (preferred port 9200)
- **Learning UI** — documentation/training portal (preferred port 9100)

The application is served by the `commerce-app` Nginx container and reverse-proxies:

- `/api/*` -> Java Spring Boot `commerce-java:8080`
- `/python/*` -> Python FastAPI `ai-python:8000`

This avoids browser CORS configuration while still keeping Java and Python as separate services.

The Docker launcher now selects `APP_PORT`, prints `APPLICATION: http://localhost:<APP_PORT>`, writes `APPLICATION_URL.txt`, and opens the application by default. `OPEN_APPLICATION.bat` always reads the selected port from `.env.local`.
