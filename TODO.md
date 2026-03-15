## Planned Features

- Docker event monitoring
- External hash anchoring 
    - I like these words: "providing persistent, transparent, immutable, and multi-dimensional verifiable log storage"
- CLI interface? or web app using flask?
- Append-only log storage
- Remote verification tools
- notification system


## Core Historian Features (High Priority)

- [ ] **Docker Event Monitoring:** Implement the background listener for the Docker socket (`/var/run/docker.sock`).
- [ ] **Cryptographic Chaining:** Finalize the SHA-256 "next-block" logic to bind log entries.
- [ ] **Append-Only Storage:** Ensure the ledger file is handled with strict append permissions to prevent accidental overwrites.
- [ ] **Integrity Verification Tool:** Create a standalone script (`verify.py`) that re-hashes the entire chain to detect historical deviations.

## Connectivity & Alerting (Medium Priority)

- [ ] **Notification System:** Integrate `ntfy.sh` or webhooks to alert on "Chain Break" or specific keywords.
- [ ] **External Hash Anchoring:** Implement a system for "providing persistent, transparent, immutable, and multi-dimensional verifiable log storage" (e.g., occasional anchoring to a git commit or external DB).
- [ ] **Web Dashboard:** Build a lightweight **Flask** web app to visualize the log history and chain health.

## Validation & UX (Low Priority)

- [ ] **Red-Team Simulation:** Write scripts to simulate log tampering (editing the file) to prove the system detects it.
- [ ] **Automated Setup:** Finalize the `setup_pi.sh` script for easy deployment on Raspberry Pi/Edge devices.
- [ ] **Documentation:** Complete the move of academic requirements into `/docs`.
