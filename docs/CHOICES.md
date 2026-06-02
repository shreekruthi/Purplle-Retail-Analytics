# ENGINEERING CHOICES

## Retail Store Analytics Platform

This document explains the major technical decisions made during implementation.

---

# Choice 1: FastAPI

## Selected

FastAPI

## Alternatives Considered

* Flask
* Django

## Reason

FastAPI provides:

* High performance
* Automatic OpenAPI generation
* Strong validation using Pydantic
* Easy Swagger integration

Result:

Faster development and easier testing.

---

# Choice 2: PostgreSQL

## Selected

PostgreSQL

## Alternatives Considered

* MySQL
* SQLite
* MongoDB

## Reason

PostgreSQL offers:

* Reliable ACID transactions
* JSON support
* Strong aggregation capabilities
* Excellent analytics support

Result:

Suitable for event storage and reporting.

---

# Choice 3: YOLOv8

## Selected

YOLOv8

## Alternatives Considered

* Haar Cascades
* SSD
* Faster R-CNN

## Reason

YOLOv8 provides:

* Fast inference
* Good accuracy
* Easy deployment
* Lightweight models available

Result:

Real-time capable visitor detection.

---

# Choice 4: ByteTrack

## Selected

ByteTrack via Supervision

## Alternatives Considered

* DeepSORT
* SORT

## Reason

ByteTrack provides:

* Stable tracking
* Good accuracy
* Easy integration

Result:

Consistent visitor IDs.

---

# Choice 5: Event-Driven Design

## Selected

Event generation architecture.

Example events:

* ENTRY
* EXIT
* ZONE_DWELL
* BILLING_QUEUE_JOIN

## Reason

Events are reusable.

Multiple analytics can be built from the same event stream.

Result:

Flexible architecture.

---

# Choice 6: Session Table

## Selected

Separate session storage.

## Reason

Avoid expensive aggregation queries on raw events.

Allows:

* Faster metrics
* Faster funnel calculations

Result:

Improved performance.

---

# Choice 7: Docker Deployment

## Selected

Docker Compose

## Reason

Ensures:

* Reproducible environment
* Easy evaluation
* One-command startup

Command:

```bash
docker compose -f deployment/docker-compose.yml up
```

Result:

Simple deployment process.

---

# Choice 8: REST APIs

## Selected

REST architecture.

## Reason

Simple integration with:

* Dashboards
* Mobile apps
* Reporting tools

Result:

Industry-standard interface.

---

# Choice 9: UUID Event IDs

## Selected

UUID

## Reason

Guarantees uniqueness.

Prevents duplicate event insertion.

Result:

Reliable ingestion.

---

# Choice 10: Pytest Testing

## Selected

Pytest

## Reason

Simple and widely adopted.

Covered:

* Metrics endpoint
* Funnel endpoint
* Anomaly endpoint

Result:

Automated validation of business logic.

---

# Trade-Offs

## Accuracy vs Speed

Decision:

Use YOLOv8n.

Advantage:

* Faster processing

Disadvantage:

* Slightly lower accuracy than larger models

Reason:

Suitable for real-time retail analytics.

---

## Simplicity vs Complexity

Decision:

Use manually defined zones.

Advantage:

* Easy implementation

Disadvantage:

* Requires manual configuration

Reason:

Adequate for assignment scope.

---


---

# Final Justification

The selected architecture prioritizes:

1. Simplicity
2. Reliability
3. Scalability
4. Maintainability
5. Ease of deployment

The final solution successfully satisfies all assignment requirements while remaining extensible for production-scale deployment.
