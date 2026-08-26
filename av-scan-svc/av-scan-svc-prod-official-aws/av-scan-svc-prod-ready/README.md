# AV Scan Service - Production Ready Baseline

## Design

`ROUTES` contains only incoming/public gateway paths.

Example:

```text
/secure-messages-svc/secure-message/members/messages/attachments
```

The same route is used for:

1. FastAPI route registration.
2. Downstream URL creation.

The first path segment is the downstream service:

```text
secure-messages-svc
```

The remaining path is the downstream path:

```text
/secure-message/members/messages/attachments
```

With:

```env
ENVIRONMENT=prod
DOWNSTREAM_URL_TEMPLATE=http://{service}.namespace-{env}.local:8080{path}
```

the downstream URL becomes:

```text
http://secure-messages-svc.namespace-prod.local:8080/secure-message/members/messages/attachments
```

## Request flow

```text
NGINX
  -> FastAPI
  -> S3
  -> AV authentication/scan
  -> downstream service
```

NGINX is responsible for the 9 MB request-body limit.

The application reads the accepted file into memory once because the maximum file size is 9 MB.

## HTTPX pools

- AV authentication: separate AsyncClient
- AV scan: separate AsyncClient
- Each downstream origin: separate AsyncClient
- Multiple routes to one downstream service share its pool
- Clients are created once during startup and closed during shutdown

## AWS

The project uses the official AWS Python SDK, `boto3`. Because boto3 is synchronous, AWS calls are executed with `asyncio.to_thread()` so they do not block the FastAPI event loop.


Local:

```env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

Production/EKS:

- Do not put access keys in the pod.
- Use EKS IAM role / Pod Identity / IRSA.

Secret name:

```text
symantic
```

Expected JSON:

```json
{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret"
}
```

## Logging

Logs include:

- x-tps-value-id
- route
- selected downstream
- S3 duration
- AV duration
- downstream duration
- total request duration
- exceptions with traceback

Secrets, access keys, tokens and file contents are not logged.

## Health

```text
GET /health/live
GET /health/ready
```

Readiness becomes successful only after startup resources are initialized.

## Worker model

Use one async Uvicorn worker per pod initially:

```text
Pod
└── Uvicorn worker
    └── FastAPI event loop
```

Scale pods horizontally with Kubernetes/HPA.

## Run locally

```bash
pip install -r requirements.txt
cp .env.example .env
python src/av-scan-svc.py
```

## Test

```bash
pytest
```
