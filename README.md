# 🎮 TDS Game: Optimized 3-Tier Cloud Architecture

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Docker](https://img.shields.io/badge/Docker-Multi--Stage-blue) ![AWS](https://img.shields.io/badge/AWS-t3.micro-orange)

A production-ready 3-tier web application deployed on AWS. This project demonstrates advanced **Cloud Optimization** techniques, successfully running a full stack (Load Balancer, Multiple App Instances, Database) on resource-constrained hardware (t3.micro) through efficient containerization and automation.

## 🏗️ Architecture Overview

The system follows a strict **3-Tier Architecture** designed for high availability and security:

* **Tier 1: Web/Proxy (Nginx):** Configured as a **Reverse Proxy** and **Load Balancer**. It sanitizes incoming traffic and distributes requests using a Round-Robin algorithm to backend containers.
* **Tier 2: Application (Flask):** Python-based REST API running in multiple replicas to handle game logic.
* **Tier 3: Database (MySQL):** A custom-engineered MySQL 8.0 image ensuring data persistence and integrity.

![Architecture Diagram](./path-to-your-architecture-diagram.png)
*(Note: Upload your architecture diagram to the repo and link it here)*

---

## ⚡ Key Optimizations (The "t3.micro" Challenge)

Deploying a full stack on an AWS **t3.micro (1GB RAM, Limited Storage)** presents significant resource challenges. I solved these using specific DevOps strategies:

### 1. 🐳 Multi-Stage Docker Builds
To prevent disk exhaustion and server freezing:
* Implemented **Multi-Stage Builds** for the Flask application.
* Stripped away compilers and build dependencies in the final image.
* **Result:** Reduced image size by over **60%**, allowing fast deployments and minimal storage footprint.

### 2. ⚖️ Nginx Load Balancing & Reverse Proxy
* Instead of exposing the application directly, **Nginx** sits in front as a Reverse Proxy.
* It efficiently handles static files and routes API traffic, reducing the processing load on the Python application servers.

### 3. 🛡️ Custom Image Engineering
* Created specific, optimized `Dockerfile`s for Nginx, App, and MySQL rather than using generic heavy images.

---

## 🛠️ Tech Stack

* **Cloud:** AWS EC2 (t3.micro)
* **Containerization:** Docker, Docker Compose
* **Orchestration:** Ansible (Infrastructure as Code)
* **CI/CD:** GitHub Actions
* **Backend:** Python Flask
* **Frontend:** Nginx, HTML5, JavaScript
* **Database:** MySQL 8.0

---

## 🚀 CI/CD Pipeline & Automation

The project utilizes a fully automated pipeline (`.github/workflows/ci-cd.yml`):

1.  **Build:** Code is pushed to GitHub.
2.  **Optimize:** Docker images are built using multi-stage processes.
3.  **Push:** Images are pushed to Docker Hub.
4.  **Deploy:** GitHub Actions triggers **Ansible** on the AWS EC2 instance.
5.  **Smart Pruning:** Ansible logic checks disk space before pulling to prevent server freezes during updates.

---

## 🔐 Security

* **Secrets Management:** All sensitive data (Database passwords, SSH keys, Docker credentials) are managed via **GitHub Secrets**.
* **Private Networking:** The Database is isolated in a private Docker network, accessible only by the App containers, not the public internet.

---

## 📥 Getting Started (Local)

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/lakshh1928/Game-TDs.git](https://github.com/lakshh1928/Game-TDs.git)
    cd Game-TDs
    ```

2.  **Configure Environment**
    Create a `.env` file:
    ```env
    MYSQL_ROOT_PASSWORD=password
    MYSQL_DATABASE=tds_db
    ```

3.  **Run with Docker Compose**
    ```bash
    docker compose up -d --build
    ```

4.  **Access the Game**
    Visit `http://localhost` in your browser.

---

## 👨‍💻 Author

**Lakshh**
* **Focus:** DevOps, Cloud Optimization, and Automation
* **Portfolio:** [Link to your LinkedIn or Portfolio]

---
