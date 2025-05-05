# 🔍 Distributed Website Health Checks with k6

This project uses [Grafana k6](https://k6.io/) to run **scalable HTTP health checks** against hundreds of endpoints across multiple teams and services. It's designed to be simple, composable, and CI-friendly — no complex infrastructure required.
Each virtual user (VU) will run one health check in parallel.

---

## ✅ Features

- 🧪 Parallel health checks using k6 virtual users
- 📁 Per-team configuration files (no merge conflicts)
- 🧩 Automatic config merging for scalability
- 📊 Optional integration with Datadog or Prometheus (loosely coupled)
- 🐳 Easy to containerize or run in CI pipelines

---

## 📂 Directory Structure
```
k6-health-checks/
├── tests/ # One config file per team
│ ├── team-commerce.json
│ ├── team-social.json
│ └── ...
├── merged-endpoints.json # Auto-generated merged config
├── multi-health-check.js # Generic k6 test script
├── merge-configs.sh # Merges all team configs into one
└── README.md # You're here
```

---

## ⚙️ Setup Instructions

### 1. Install k6

On Ubuntu / Pop!_OS:

```bash
sudo apt update
sudo apt install gnupg curl -y
curl -s https://dl.k6.io/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/k6-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt update
sudo apt install k6 -y
```

---

## Add Team Config Files
Each team maintains their own configs/team-*.json file:
```
[
  { "name": "My API", "url": "https://my-api.example.com/health" },
  { "name": "Docs", "url": "https://my-site.example.com/docs" }
]
```

---

## Build Process
```bash
# take all team configs and merge them into one
./build.sh
```

---

## Run the Tests
```bash
k6 run upime-check.js
```