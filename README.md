# Log Analytics Platform with PySpark on Docker Swarm

A distributed log analytics system built with Docker Swarm orchestration and PySpark for batch data processing.

## Overview

This project implements a complete data pipeline for analyzing web user behavior logs. The system ingests events through a REST API, stores them in PostgreSQL, processes them periodically using PySpark, and exposes aggregated statistics through another API.

The architecture was migrated from virtual machines to a containerized environment using **Docker Swarm**, demonstrating orchestration, scalability, and Infrastructure as Code practices.

## Architecture

The system consists of 4 main services orchestrated with Docker Swarm:

| Service          | Technology     | Role                              | Replicas |
|------------------|----------------|-----------------------------------|----------|
| `producer_api`   | Flask          | Event ingestion API               | 2        |
| `spark_processor`| PySpark        | Batch ETL processing (every 5 min)| 1        |
| `postgres`       | PostgreSQL 14  | Data persistence                  | 1        |
| `dashboard`      | Flask          | Statistics query API              | 1        |

**Data Flow:**
1. Events are sent to `producer_api` → stored in `raw_events` table
2. Every 5 minutes, `spark_processor` reads raw data via JDBC
3. PySpark performs aggregations (total views + unique users per page)
4. Results are stored in `page_stats` using UPSERT
5. `dashboard` API exposes the processed statistics

## Technologies

- **Docker Swarm** — Container orchestration
- **PySpark 3.4** — Distributed data processing
- **PostgreSQL 14** — Relational database
- **Flask** — REST APIs
- **Python 3.9**

## Deployment

### Prerequisites
- Docker Engine 24+
- Docker Swarm initialized (`docker swarm init`)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/DanielAlxzBrand/docker-swarm-pyspark-log-analytics.git
cd docker-swarm-pyspark-log-analytics

# 2. Create environment file
cp .env.example .env
# Edit .env with your credentials

# 3. Deploy the stack
docker stack deploy -c docker-stack.yml log-analytics

# 4. Check services status
docker stack ps log-analytics


## API Endpoints

### Send an event

```bash
curl -X POST http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{"page":"home","user_id":"user123"}'

### Get statistics
curl http://localhost:5002/stats

Documentation
- A complete technical document is available in the docs/ folder:

- Documento Técnico (PDF)

Authors

- Daniel Alexander Brand García

Notes
- The PySpark job runs every 5 minutes automatically.
- The system uses idempotent UPSERT operations to ensure data consistency.
- All services communicate through an internal overlay network