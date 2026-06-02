# Retail Store Analytics Platform

# Running the Project

## Build Docker Containers

```bash
docker compose -f deployment/docker-compose.yml build
```

---

## Start Containers

```bash
docker compose -f deployment/docker-compose.yml up
```

---

## Verify Containers

```bash
docker ps
```

Expected:

```text
deployment-api-1
deployment-db-1
```

---

# Running Analytics Pipeline

## Visitor Tracking

```bash
cd pipeline

python run.py
```

Generates ENTRY and EXIT events.

---

## Zone Analytics

```bash
python run_dwell.py
```

Generates ZONE_DWELL events.

---

## Queue Analytics

```bash
python run_queue.py
```

Generates BILLING_QUEUE_JOIN events.

---

## Feed Events Into API

```bash
python test_feed.py
```

Expected:

```json
{
  "received": 4,
  "inserted": 4,
  "duplicates": 0,
  "failed": 0
}
```

---

# Testing

Run inside Docker:

```bash
docker exec -it deployment-api-1 python -m pytest tests -v
```

Expected:

```text
tests/test_anomalies.py PASSED
tests/test_funnel.py PASSED
tests/test_metrics.py PASSED

3 passed
```

---

## Overview

Retail Store Analytics Platform is a computer-vision powered analytics system for Purplle retail stores.

The system processes CCTV footage from multiple cameras, detects visitors, tracks movement, generates behavioral events, stores analytics data in PostgreSQL, and exposes insights through FastAPI endpoints.

Features implemented:

* Visitor Detection
* Multi-Object Tracking
* Session Tracking
* Event Ingestion
* Zone Dwell Analytics
* Queue Analytics
* Funnel Analytics
* Heatmap Analytics
* Anomaly Detection
* Dockerized Deployment
* Automated Testing

---

# Architecture

```text
CCTV Cameras
      |
      v
YOLOv8 Person Detection
      |
      v
Object Tracking
      |
      v
Event Generation Pipeline
      |
      v
FastAPI Ingestion API
      |
      v
PostgreSQL Database
      |
      +-------------------+
      |                   |
      v                   v
Analytics APIs      Dashboard Layer
```

---

# Technology Stack

## Backend

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL

## Computer Vision

* OpenCV
* YOLOv8
* Supervision Tracker

## Deployment

* Docker
* Docker Compose

## Testing

* Pytest

---

# Project Structure

```text
PURPLLE
│
├── app
│   ├── core
│   ├── database
│   ├── models
│   ├── routers
│   ├── services
│   └── main.py
│
├── pipeline
│   ├── detect.py
│   ├── tracker.py
│   ├── emit.py
│   ├── event_logic.py
│   ├── dwell_logic.py
│   ├── queue_logic.py
│   ├── run.py
│   ├── run_dwell.py
│   └── run_queue.py
│
├── tests
│   ├── test_metrics.py
│   ├── test_funnel.py
│   └── test_anomalies.py
│
├── deployment
│   └── docker-compose.yml
│
├── data
│   └── CCTV videos
│
└── README.md
```

---

# Database Design

## events table

Stores all generated visitor events.

### Columns

| Column        | Type      |
| ------------- | --------- |
| event_id      | UUID      |
| store_id      | String    |
| camera_id     | String    |
| visitor_id    | String    |
| event_type    | String    |
| zone_id       | String    |
| dwell_ms      | Integer   |
| confidence    | Float     |
| timestamp     | Timestamp |
| metadata_json | JSON      |

---

## sessions table

Stores visitor sessions.

### Columns

| Column         | Type      |
| -------------- | --------- |
| session_id     | UUID      |
| store_id       | String    |
| visitor_id     | String    |
| entry_time     | Timestamp |
| exit_time      | Timestamp |
| total_dwell_ms | Integer   |
| zones_visited  | JSON      |
| converted      | Boolean   |
| is_staff       | Boolean   |

---

# Event Types

## ENTRY

Generated when a visitor enters the store.

Example:

```json
{
  "event_type": "ENTRY"
}
```

---

## EXIT

Generated when a visitor exits the store.

```json
{
  "event_type": "EXIT"
}
```

---

## ZONE_DWELL

Generated when a visitor remains in a zone.

```json
{
  "event_type": "ZONE_DWELL",
  "zone_id": "SKINCARE"
}
```

---

## BILLING_QUEUE_JOIN

Generated when a visitor joins billing queue.

```json
{
  "event_type": "BILLING_QUEUE_JOIN"
}
```

---

# Analytics APIs

Base URL:

```text
http://localhost:8000
```

---

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Event Ingestion

```http
POST /events/batch
```

Response:

```json
{
  "received": 4,
  "inserted": 4,
  "duplicates": 0,
  "failed": 0,
  "errors": []
}
```

---

## Metrics API

```http
GET /stores/ST1008/metrics
```

Response:

```json
{
  "unique_visitors": 5,
  "total_sessions": 5,
  "conversion_rate": 0,
  "avg_session_minutes": 5,
  "avg_dwell_per_zone": {
    "SKINCARE": "33.50",
    "MAKEUP": "60.00"
  },
  "queue_depth": 2,
  "abandonment_rate": 0
}
```

---

## Funnel API

```http
GET /stores/ST1008/funnel
```

Response:

```json
{
  "visitors": 5,
  "zone_visitors": 2,
  "queue_visitors": 2,
  "converted_visitors": 0,
  "visitor_to_zone": 40.0,
  "zone_to_queue": 100.0,
  "queue_to_purchase": 0.0
}
```

---

## Heatmap API

```http
GET /stores/ST1008/heatmap
```

Response:

```json
{
  "zones": {
    "SKINCARE": 2,
    "MAKEUP": 1
  }
}
```

---

## Anomalies API

```http
GET /stores/ST1008/anomalies
```

Response:

```json
{
  "anomalies": [
    {
      "type": "DEAD_ZONE",
      "severity": "LOW",
      "message": "No customer activity detected"
    }
  ]
}
```

---

# Pipeline Components

## Phase 1 – Detection

Uses YOLOv8 to detect people from CCTV footage.

File:

```text
pipeline/detect.py
```

Output:

```text
Bounding boxes of detected people
```

---

## Phase 2 – Tracking

Uses Supervision ByteTrack tracker.

File:

```text
pipeline/tracker.py
```

Output:

```text
Persistent Visitor IDs
```

Example:

```text
VIS_1
VIS_2
VIS_3
```

---

## Phase 3 – Event Generation

Files:

```text
pipeline/event_logic.py
pipeline/run.py
```

Generated events:

* ENTRY
* EXIT

---

## Phase 4 – Zone Dwell Analytics

Files:

```text
pipeline/dwell_logic.py
pipeline/run_dwell.py
```

Generated events:

```text
ZONE_DWELL
```

Example:

```text
SKINCARE
MAKEUP
```

---

## Phase 5 – Queue Analytics

Files:

```text
pipeline/queue_logic.py
pipeline/run_queue.py
```

Generated events:

```text
BILLING_QUEUE_JOIN
```

---
# Sample CCTV videos were provided as part of the challenge dataset and are intentionally excluded from the repository because of GitHub file size limits.

# Assumptions

1. Each tracked person corresponds to one visitor.
2. Visitor IDs remain stable during tracking.
3. Zone definitions are manually configured.
4. Billing queue region is predefined.
5. Staff classification is not implemented and defaults to false.
6. Purchase conversion events are not available from POS integration.

---

# Design Choices

## YOLOv8

Chosen because:

* Fast inference
* Lightweight
* Good person detection accuracy

---

## FastAPI

Chosen because:

* High performance
* Automatic Swagger documentation
* Built-in validation
* Easy API development

---

## PostgreSQL

Chosen because:

* Reliable relational database
* JSON support
* Aggregation-friendly

---

## Docker

Chosen because:

* Easy deployment
* Reproducible environment
* Evaluator can run with one command

---

