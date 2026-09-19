# Log-Analytics-Engine

A scalable log analytics engine built in Python for processing large-scale
application and infrastructure logs.

## Goals

- Process 10GB+ log datasets
- Stream logs without loading entire files into memory
- Parse structured and semi-structured logs
- Calculate performance indicators
- Detect anomalous behavior
- Store analytical results efficiently
- Expose metrics for observability
- Scale from a single machine to distributed processing

## Planned Stack

- Python
- FastAPI
- Nginx
- Polars
- PyArrow
- DuckDB
- PostgreSQL
- Prometheus
- Grafana
- Docker
- Kafka
- Apache Spark
- PySpark

## Architecture

```text
Traffic
   ↓
Application
   ↓
Raw Logs
   ↓
Ingestion
   ↓
Parsing
   ↓
Aggregation
   ↓
Analytics
   ↓
Storage
   ↓
Observability