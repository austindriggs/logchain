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


## Project Structure Reference

This is the target layout for the **LogChain** repository:

```bash
logchain/
├── docs/                   # Documentation & Academic requirements
│   └── proposal.md         # CPE 493 Project Proposal
├── src/                    # Core source code
│   ├── agent.py            # Main background service (Docker stream listener)
│   ├── chain.py            # Hashing logic and Ledger management
│   ├── alerts.py           # Notification triggers (ntfy.sh, etc.)
│   └── config.py           # Watch-list keywords and API keys
├── tools/                  # Utility scripts
│   ├── verify.py           # CLI tool to check log integrity/detect tampering
│   └── setup_pi.sh         # Script to automate Docker/User setup
├── tests/                  # Red-Team / Validation testing
│   ├── inject_log.py       # Script to generate dummy container logs
│   └── tamper_test.sh      # Script to simulate an attacker (sed/rm -rf)
├── docker-compose.yml      # Orchestration for the Historian
├── Dockerfile              # Debian-based build instructions
├── README.md               # Project overview
└── requirements.txt        # Python dependencies (docker, pyyaml, flask)
```

## NOTES

an example
```
logchain/
├── docs/                   # Documentation & Academic requirements
│   └── proposal.md         # Your original project proposal
├── src/                    # Core source code
│   ├── __init__.py
│   ├── agent.py            # Main background service (Docker stream listener)
│   ├── chain.py            # Hashing logic and Ledger management
│   ├── alerts.py           # Notification triggers (ntfy.sh, etc.)
│   └── config.py           # Watch-list keywords and API keys
├── tools/                  # Utility scripts for the project
│   ├── verify.py           # CLI tool to check log integrity/detect tampering
│   └── setup_pi.sh         # Shell script to automate Docker/User setup
├── tests/                  # Red-Team / Validation testing
│   ├── inject_log.py       # Script to generate dummy container logs
│   └── tamper_test.sh      # Script to simulate an attacker (sed/rm -rf)
├── .gitignore              # Ignore venv/, __pycache__/, and .env
├── README.md               # The project overview we just drafted
└── requirements.txt        # Python dependencies
```

