# Fault-Tolerant RabbitMQ Event Processor

A production-inspired event-driven microservices project built with **RabbitMQ**, **Docker Compose**, and **Python** that demonstrates asynchronous communication, service decoupling, fault tolerance, and scalable messaging architecture.

---

# Overview

Modern applications are composed of multiple independent microservices. Instead of communicating directly with each other, they exchange events through a message broker such as RabbitMQ.

This project simulates a real-world event-driven architecture where multiple services independently consume events produced by a central producer.

Currently, the project consists of:

- Producer Service
- RabbitMQ Message Broker
- Email Consumer
- Analytics Consumer
- Notification Consumer

Each service runs in its own Docker container and communicates asynchronously through RabbitMQ.

---

# Problem Statement

In traditional systems, services often communicate directly.

```
Order Service
      │
      ├── Email Service
      ├── Analytics Service
      ├── Notification Service
      ├── Billing Service
      └── Inventory Service
```

As the application grows, the producer becomes tightly coupled with every service.

Problems include:

- High service dependency
- Difficult scalability
- Complex deployments
- Poor fault tolerance
- Hard to introduce new services

---

# Solution

Instead of communicating directly, services exchange events through RabbitMQ.

```
                    Producer
                        │
                        ▼
                 RabbitMQ Exchange
           ┌──────────┼──────────┐
           ▼          ▼          ▼
     Email Queue Analytics Queue Notification Queue
           ▼          ▼          ▼
     Email Service Analytics Service Notification Service
```

Each microservice is completely independent.

New services can be added without modifying existing consumers.

---

# Features

- Asynchronous Event Processing
- Event-Driven Architecture
- RabbitMQ Direct Exchange
- Multiple Independent Consumers
- Durable Queues
- Persistent Messages
- Automatic RabbitMQ Connection Retry
- Automatic Reconnection on Failure
- Dockerized Microservices
- Health Checks
- Restart Policies
- Environment Variable Configuration
- Fault-Tolerant Messaging
- Containerized Deployment

---

# Tech Stack

- Python 3.12
- RabbitMQ
- Docker
- Docker Compose
- Pika (RabbitMQ Python Client)

---

# Project Structure

```

Fault-Tolerant-RabbitMQ-Event-Processor/

├── producer/
│ ├── producer.py
│ ├── Dockerfile
│ └── requirements.txt
│
├── consumers/
│ ├── email/
│ ├── analytics/
│ └── notification/
│
├── docker-compose.yml
├── README.md
└── docs/

```

---

# How It Works

Every few seconds the Producer generates an order event.

The producer publishes three different events:

- Email Event
- Analytics Event
- Notification Event

RabbitMQ routes each event to the appropriate queue using routing keys.

Each consumer listens only to its assigned queue.

```

Producer

↓

RabbitMQ Direct Exchange

↓

routing=email → email_queue → Email Consumer

↓

routing=analytics → analytics_queue → Analytics Consumer

↓

routing=notification → notification_queue → Notification Consumer

```

This architecture keeps services loosely coupled and independently scalable.

---

# Getting Started

## Clone the Repository

```bash
git clone https://github.com/saiganesh74/Fault-Tolerant-RabbitMQ-Event-Processor.git

cd Fault-Tolerant-RabbitMQ-Event-Processor
```

---

## Start the Project

```bash
docker compose up --build -d
```

---

## Verify Running Containers

```bash
docker ps
```

You should see:

- rabbitmq
- producer
- consumer
- analytics
- notification

---

## View Producer Logs

```bash
docker logs -f producer
```

---

## View Email Consumer

```bash
docker logs -f consumer
```

---

## View Analytics Consumer

```bash
docker logs -f analytics
```

---

## View Notification Consumer

```bash
docker logs -f notification
```

---

## Stop Everything

```bash
docker compose down
```

---

# RabbitMQ Management Dashboard

RabbitMQ Management UI is available at

```
http://localhost:15672
```

Default credentials:

```
Username : guest
Password : guest
```

---

# Current Workflow

```

Producer

│

├── Email Event ─────────► Email Queue ─────────► Email Consumer

│

├── Analytics Event ─────► Analytics Queue ─────► Analytics Consumer

│

└── Notification Event ──► Notification Queue ──► Notification Consumer

```

---

# Fault Tolerance

The project automatically handles failures by:

- Retrying RabbitMQ connection until available
- Reconnecting after broker restart
- Durable queues survive RabbitMQ restarts
- Persistent messages prevent data loss
- Docker restart policies automatically restart containers

---

# Future Enhancements

The project will continue evolving into a production-grade messaging platform.

Upcoming improvements include:

## RabbitMQ

- Fanout Exchange
- Topic Exchange
- Dead Letter Queue (DLQ)
- Retry Queues
- Delayed Messages
- Message TTL
- Priority Queues
- Publisher Confirms
- Consumer Prefetch

## Monitoring

- Prometheus
- Grafana
- RabbitMQ Exporter
- Queue Monitoring
- Consumer Metrics
- Alerting

## Reliability

- Chaos Engineering
- Network Failure Simulation
- Container Failure Testing
- High Availability RabbitMQ Cluster

## Security

- TLS Encryption
- RabbitMQ Authentication
- Authorization
- Secrets Management

## Deployment

- Kubernetes
- Helm Charts
- Horizontal Pod Autoscaling
- GitHub Actions CI/CD
- ArgoCD GitOps

---

# Learning Outcomes

This project demonstrates practical knowledge of:

- Event-Driven Architecture
- RabbitMQ
- Docker
- Docker Compose
- Message Routing
- Microservices
- Fault Tolerance
- Container Networking
- Durable Messaging
- Asynchronous Communication
- Production-Oriented System Design

---

# Contributing

Contributions, feature requests, and improvements are welcome.

Feel free to fork the repository and submit a pull request.

