# 🔍 Distributed Website Health Checks with k6 & Otel Collector

This project uses [Grafana k6](https://k6.io/) to run **scalable HTTP health checks** against hundreds of endpoints across multiple teams and services. It's designed to be simple, composable, and CI-friendly — no complex infrastructure required.
Each virtual user (VU) will run one health check in parallel.

Health checks are pushed to an Otel Collector, which can then be configured to send metrics to various backends like 
Datadog or Prometheus. An example Otel Collector config is provided in the `otel-collector` directory.

---

## ✅ Features

- 🧪 Parallel health checks using k6 virtual users
- 📁 Per-team configuration files (no merge conflicts)
- 🧩 Automatic config merging for scalability
- 🐳 Easy to containerize or run in CI pipelines
- 📊 Built-in report scripts to validate OTEL Collector
- 📊 Optional integration with Datadog or Prometheus (loosely coupled)


---

## 📂 k6-runner Directory Structure
```
k6-health-checks/
├── tests/ # One config file per team
│ ├── team-commerce.json
│ ├── team-social.json
│ └── ...
├── merged-endpoints.json # Auto-generated merged config
├── multi-health-check.js # Generic k6 test script
└── build.sh # Merges all team configs into one
```

📂 otel-collector Directory Structure
```
otel-collector/
├── Dockerfile # Dockerfile for the Otel Collector
└── otel-collector-config.yaml # Example config for the Otel Collector
```

---

## ⚙️ Setup Instructions

### 🧩 Modify Team Config Files
Each team maintains their own tests/*.json file by submitting files via merge request:
```
[
  { "name": "My API", "url": "https://my-api.example.com/health" },
  { "name": "Docs", "url": "https://my-site.example.com/docs" }
]
```

---

## 🚀 Run the Containers
```bash
docker compose up
```

## 📊 Report on OTEL Collector
This is still a bit crude and requies `pip install pandas`
```bash
./reports/summary.py

# or 
./reports/timeseries.py