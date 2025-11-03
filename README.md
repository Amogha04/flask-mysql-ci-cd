# Flask + MySQL (Docker Compose) — CI/CD with Jenkins & Docker Hub

## Project overview
This project demonstrates a multi-container web application (Python Flask + MySQL) managed with Docker Compose, and a CI/CD pipeline using GitHub, Jenkins, and Docker Hub.

**Features**
- Flask web application that records and returns visit counts.
- MySQL database container with environment-configured user, password and database.
- `docker-compose.yml` to bring up both services on a shared network.
- Jenkins pipeline that builds the image, pushes to Docker Hub and (optionally) deploys via `docker compose`.
- Demonstrates container networking, environment variables, and automated CI/CD.

## Repository structure
```
flask-mysql-ci-cd/
├─ app.py
├─ Dockerfile
├─ requirements.txt
├─ docker-compose.yml
├─ Jenkinsfile
├─ README.md
```

## Prerequisites
- Docker Desktop (Windows/macOS) or Docker Engine + Docker Compose (Linux)
- Git
- Jenkins (for CI/CD) — this repo includes a Jenkinsfile for a pipeline
- Docker Hub account

## Local run (development)
1. Ensure Docker is running.
2. From project root:
   ```bash
   docker compose down -v
   docker compose up --build
   ```
3. Open: `http://localhost:5000`  
   You should see JSON like:
   ```json
   {"status":"ok","db_host":"db","visits":1}
   ```
   Refresh to increase the visits count.

## Docker Compose details
* `web` service: Flask app (exposes port `5000`)
* `db` service: MySQL 8 with `--default-authentication-plugin=mysql_native_password`
* Data persisted with a Docker volume `db_data`

## CI/CD (Jenkins) — high level
1. Jenkins job configured as Pipeline (Multibranch or single pipeline) that reads `Jenkinsfile` from repo.
2. Pipeline steps:
   * Checkout code
   * Authenticate to Docker Hub (credentials stored in Jenkins)
   * Build Docker image (`amogha04/flask-mysql-ci-cd:latest`)
   * Push image to Docker Hub
   * (Optional) Run `docker compose up -d --build` to deploy on target server

> **Security**: Docker Hub credentials are stored in Jenkins Credentials Manager (Username + Password / Access Token).  
> Do NOT store secrets in the repo.

## How to trigger CI automatically
1. In GitHub repo → Settings → Webhooks
2. Add webhook: `http://<JENKINS_HOST>:<JENKINS_PORT>/github-webhook/` with payload `application/json`
3. On push, Jenkins picks up the change and runs the pipeline.

## Verification checklist (take screenshots for submission)
1. `docker ps` showing `flask-web` and `mysql-db` running.
2. Browser open at `http://localhost:5000` showing JSON with increasing `visits`.
3. Jenkins pipeline run console showing `Build`, `Docker login`, `Push` stages succeeding.
4. Docker Hub repository showing the pushed image/tag.
5. `docker network inspect` showing both containers on the same network (optional).

## Troubleshooting
* If Flask shows `Can't connect to MySQL`: wait for DB to initialize or restart with  
  `docker compose down -v && docker compose up --build`
* If MySQL auth error `Plugin 'mysql_native_password' is not loaded`: ensure MySQL service includes:
  ```yaml
  command: --default-authentication-plugin=mysql_native_password
  ```
* If Jenkins cannot run Docker commands: run Jenkins container with Docker socket mounted and install Docker CLI inside Jenkins, and store Docker Hub token in Jenkins Credentials.

## References
- [Flask](https://palletsprojects.com/p/flask/)
- [MySQL Docker images](https://hub.docker.com/_/mysql)
- [Docker Compose file reference](https://docs.docker.com/compose/compose-file/)
- [Jenkins Pipelines](https://www.jenkins.io/doc/book/pipeline/getting-started/#getting-started-with-pipelines-in-jenkins)
