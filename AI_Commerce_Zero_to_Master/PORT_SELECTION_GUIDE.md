# Port Selection Guide — Docker v1.2

The local Docker deployment supports **two port modes**.

## 1. Automatic ports — easiest

Double-click:

- `START_LOCAL_DOCKER.bat`
- `START_FULL_LOCAL_DOCKER.bat`

The launcher checks the preferred Windows host port first. If occupied, it selects another free port automatically.

Examples:

```text
Java API: preferred 8080 -> if busy, 8081 -> 8082 -> 18080 -> nearby free port
Python AI: preferred 8000 -> if busy, 8001 -> 8002 -> 18000 -> nearby free port
Learning: preferred 9100 -> if busy, 9101 -> 9102 -> 19100 -> nearby free port
```

## 2. Interactive ports — choose yourself

Double-click:

- `START_LOCAL_DOCKER_INTERACTIVE.bat`
- `START_FULL_LOCAL_DOCKER_INTERACTIVE.bat`

For each service you see:

```text
[Python AI API]
Preferred port 8000 is OCCUPIED.
Suggested free port: 8001
Enter host port, or press Enter to use 8001:
```

You can type, for example:

```text
18000
```

The launcher checks that:

- the value is a valid TCP port,
- Windows is not already using it,
- another AI Commerce service has not already selected it.

## Host port vs container port

You are changing only the **Windows host port**.

```text
Windows                       Docker network
localhost:18000  ---------->  ai-python:8000
localhost:18080  ---------->  commerce-java:8080
localhost:16333  ---------->  qdrant:6333
localhost:15432  ---------->  postgres:5432
```

This is why Java can always call `http://ai-python:8000` internally even if you choose `18000` on Windows.

## Where selected ports are saved

The launcher writes them to:

```text
.env.local
```

Double-click:

```text
SHOW_SELECTED_PORTS.bat
```

to display them.

## Diagnostics

If a container fails:

```text
DOCKER_STATUS.bat
```

shows selected ports, all container states, Python logs and Java logs.

For the Python service, v1.2 also initializes Qdrant/pgvector lazily so the FastAPI `/health` endpoint is not blocked while a vector backend is warming up.


ACTUAL APPLICATION UI
---------------------
Preferred application URL: http://localhost:9200
The deployment launcher selects APP_PORT automatically (or interactively) and prints the exact APPLICATION URL.
Use OPEN_APPLICATION.bat to open the selected application port.
The learning portal is separate (preferred http://localhost:9100).
