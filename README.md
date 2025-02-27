# TerraScale: Planet-Scale Social Network Simulation

This repository is a thought exercise to design and simulate a planet-scale social network architecture. It includes:

- An **ARCHITECTURE.md** document that details the system design.
- A sample **User Service** implemented as a Flask application.
- A **docker-compose.yml** file to run core components locally (User Service, PostgreSQL, Kafka, Redis).

## How to Run Locally

1. **Prerequisites:**

   - Docker and Docker Compose must be installed.

2. **Launch the System:**  
   Run the following command in the repository root:
   ```bash
   docker-compose up --build
   ```

This will start:

- The user-service container (accessible on port 5000).
- PostgreSQL for data storage.
- Kafka (and Zookeeper) for event streaming.
- Redis for caching.

3. **Explore the Code:**

- The User Service is located in `services/user-service/`.
- Extend the service or add new microservices following the patterns provided.

## Future Work

- Extend the implementation to include additional services (Post Service, Feed Service, etc.).
- Create Kubernetes manifests for multi-region deployment simulations.
- Add CI/CD pipelines and advanced observability configurations.

Feel free to contribute, extend, or use this repository as a basis for your experiments in planet-scale architecture!
