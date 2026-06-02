# DESIGN DOCUMENT

## Retail Store Analytics Platform

### Objective

The objective of this system is to transform raw CCTV footage into actionable retail analytics.

The platform detects visitors, tracks movement through the store, generates behavioral events, stores those events in a database, and exposes analytics through REST APIs.

---

# High Level Architecture

```text
CCTV Cameras
      |
      v
YOLOv8 Detection
      |
      v
Visitor Tracking
      |
      v
Event Generation
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
Analytics APIs      Dashboard
```

---

# Component Design

## 1. Detection Layer

### Purpose

Detect people from CCTV footage.

### Implementation

File:

pipeline/detect.py

Technology:

* YOLOv8

Input:

* Video frame

Output:

* Bounding boxes

Example:

```text
Person A → [100,120,250,420]
Person B → [320,110,500,430]
```

---

## 2. Tracking Layer

### Purpose

Assign stable IDs to visitors.

### Implementation

File:

pipeline/tracker.py

Technology:

* Supervision ByteTrack

Input:

* Bounding boxes

Output:

```text
VIS_1
VIS_2
VIS_3
```

This allows a visitor to be followed across frames.

---

## 3. Event Generation Layer

### Purpose

Convert tracking information into business events.

### Files

pipeline/event_logic.py

pipeline/run.py

Generated events:

* ENTRY
* EXIT

Example:

```json
{
  "visitor_id":"VIS_1",
  "event_type":"ENTRY"
}
```

---

## 4. Zone Analytics Layer

### Purpose

Measure visitor engagement.

### Files

pipeline/dwell_logic.py

pipeline/run_dwell.py

Generated event:

ZONE_DWELL

Example:

```json
{
  "visitor_id":"VIS_2",
  "zone_id":"SKINCARE",
  "dwell_ms":12000
}
```

---

## 5. Queue Analytics Layer

### Purpose

Measure checkout congestion.

### Files

pipeline/queue_logic.py

pipeline/run_queue.py

Generated event:

BILLING_QUEUE_JOIN

Example:

```json
{
  "visitor_id":"VIS_5",
  "event_type":"BILLING_QUEUE_JOIN"
}
```

---

# Database Design

## Events Table

Stores all raw events.

Reason:

Provides complete event history.

Supports:

* Funnel analysis
* Heatmaps
* Queue analytics
* Anomaly detection

---

## Sessions Table

Stores visitor sessions.

Reason:

Analytics frequently require session-level aggregation.

Examples:

* Average session duration
* Conversion rate
* Zone engagement

---

# Analytics Design

## Metrics API

Calculates:

* Unique visitors
* Sessions
* Average dwell
* Queue depth
* Conversion rate

---

## Funnel API

Measures progression:

Visitor
→ Zone Visitor
→ Queue Visitor
→ Converted Visitor

---

## Heatmap API

Counts visits per zone.

Output:

```json
{
  "SKINCARE": 12,
  "MAKEUP": 8
}
```

---

## Anomaly API

Detects:

* Dead zones
* Low traffic
* Long queues

---

# Scalability Considerations

Current version:

* Single store
* Batch video processing

Future version:

* Multi-store support
* Real-time camera streams
* Distributed event processing
* Kafka event pipeline

---

# Reliability

Measures implemented:

* Duplicate event detection
* Database transactions
* UUID-based event IDs
* API validation using Pydantic

---

# Security

Current implementation:

* Input validation
* Structured schemas

Future enhancements:

* Authentication
* Role-based access control
* API keys
* HTTPS

---

# Testing Strategy

API testing performed using Pytest.

Covered endpoints:

* Metrics
* Funnel
* Anomalies

Result:

3/3 tests passing.
