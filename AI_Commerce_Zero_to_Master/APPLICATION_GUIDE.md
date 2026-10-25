# AI Commerce Application UI

This is the actual customer-facing commerce application, separate from the learning portal.

## Start

Run one of the Docker launchers:

- `START_LOCAL_DOCKER.bat` — core stack, automatic ports
- `START_FULL_LOCAL_DOCKER.bat` — full stack, automatic ports
- `START_LOCAL_DOCKER_INTERACTIVE.bat` — core stack, choose ports
- `START_FULL_LOCAL_DOCKER_INTERACTIVE.bat` — full stack, choose ports

The launcher prints the actual URL and opens it automatically.

Preferred URL:

`http://localhost:9200`

If 9200 is busy, a different free port is selected and saved in `.env.local` as `APP_PORT`.

You can always double-click `OPEN_APPLICATION.bat` to open the correct selected port.

## What the application does

- Browse products from Java Spring Boot `/api/products`
- Add products to a customer cart
- Run mock checkout and payment authorization/capture
- AI semantic product search through Java -> Python AI
- Customer recommendations
- AI shopping copilot / agent
- Runtime service status
- Direct links to Java/Python health and Python Swagger

## Architecture

Browser -> Commerce Nginx -> Java Spring Boot -> Python AI -> ML/Vector/RAG

The application Nginx reverse-proxies `/api/*` to the Java container and `/python/*` to the Python container, so the browser stays on one origin and does not require CORS configuration.

## Application vs learning site

- Application: `http://localhost:<APP_PORT>` (preferred 9200)
- Learning portal: `http://localhost:<LEARNING_PORT>` (preferred 9100)
- Java API: `http://localhost:<JAVA_PORT>` (preferred 8080)
- Python API: `http://localhost:<AI_PORT>/docs` (preferred 8000)
