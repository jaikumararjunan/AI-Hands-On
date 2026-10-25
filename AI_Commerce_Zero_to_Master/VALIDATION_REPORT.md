# Validation Report

Checked: 25 Oct 2026

## Release 0.3 checks completed

- AI/Python syntax compilation: **PASS**.
- Existing Python service tests: **PASS (5/5)**.
- Mock-data generator syntax: **PASS** for generator, validator, streaming simulator and running-service exerciser.
- `tiny + normal` generation: **PASS**.
- `small + mixed-chaos` generation: **PASS**.
- Cross-service referential integrity: **PASS** for customer/order/product/payment/shipment/return/inventory relationships.
- Payment idempotency-key uniqueness in generated data: **PASS**.
- JSONL validation: **PASS** for domain events, data-platform events, vector corpus and service logs.
- Learning-site JavaScript syntax: **PASS**.
- New DOCX package integrity: **PASS**.
- New DOCX visual QA: **PASS** for guide 14; every rendered page inspected.

## Existing release checks retained

- Historical Bronze -> Silver -> SQLite warehouse -> feature pipeline: previously validated.
- Marketing service smoke test: previously validated.
- JSON contracts and YAML structure: previously validated.
- Java Maven POM XML structure: previously validated.
- Payment mock-gateway design uses safe provider references, not PAN/CVV.

## Environment limitations in this build container

`mvn` and `pwsh` are not installed here. Therefore:

- Full Spring Boot Maven compilation/tests are **not claimed as executed** in this container.
- PowerShell wrappers are **not claimed as executed** in this container.

Run the full Windows validation locally:

```powershell
.\scripts\validate-project.ps1
```

## Mock-data validation commands

```powershell
.\scripts\generate-mock-data.ps1 -Profile tiny -Scenario normal

cd mock-data
python .\validate_mock_data.py
```

For a failure scenario:

```powershell
python .\generate_mock_data.py --profile small --scenario mixed-chaos --seed 7 --reset
python .\validate_mock_data.py
```

## Mock-data safety note

All generated records are synthetic. The payment domain deliberately generates provider-style references rather than real card/account credentials. The generator is intended for development, QA, training, ML experiments, RAG/vector exercises, observability labs and architecture discussions.

## v1.1 single-click Docker deployment
- Added Java multi-stage Dockerfile.
- Added Python FastAPI Dockerfile with Qdrant startup wait.
- Added unified `infra/docker-compose.local.yml`.
- Added automatic host-port selection via `scripts/start-local-docker.ps1`.
- Added one-click Windows launchers for core and full stacks.
- Added stop/status/reset scripts.
- Added Docker-native Prometheus targets.
- Static YAML and HTML link validation passed in the build environment.
- Docker daemon was not available in the build environment, so image build/runtime validation must be performed on the target Windows Docker Desktop host.

---

## v1.3 targeted validation

Latest user log root cause addressed:

- `AiServiceClient` required `RestClient.Builder` but no bean was registered.
- Added explicit `HttpClientConfig.restClientBuilder()` bean.
- Added `AiServiceClientContextTest` regression test.
- Java Docker build now runs the tests (`mvn package`).
- Java Docker health check now probes `/actuator/health`.
- Compose failure diagnostics now print both Python and Java logs.
- START_HERE.html relative links: validated, 0 broken.
- AI_Commerce_Master_Guide.html relative links: validated, 0 broken.
- Python/YAML/XML/JSON structural validation: passed in artifact build environment.

Runtime Docker execution must be verified on the user's Windows Docker Desktop host.
