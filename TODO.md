## Planned Features

- Docker event monitoring
- External hash anchoring 
    - I like these words: "providing persistent, transparent, immutable, and multi-dimensional verifiable log storage"
- CLI interface? or web app using flask?
- Append-only log storage
- Remote verification tools
- notification system


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

