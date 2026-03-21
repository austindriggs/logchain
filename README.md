# LogChain: A Lightweight Docker Historian and Alerting System

LogChain continuously monitors Docker container logs, cryptographically chains each log entry to preserve an immutable record, and alerts administrators when suspicious activity or log tampering is detected.

This system provides three main features that make it unique from other solutions:
1. Written in Python and runs in Docker, providing flexibility for small servers, edge devices, and homelabs.
2. Provides a user interface using Flask and an alerting system using ntfy.
3. Free and open sourced, allowing users and admins to preserve, backup, and restore their data as they please.


## Architecture

```mermaid
graph TD
    subgraph Docker_Environment [External Environment]
        D[Docker Daemon]
        C1[Container A]
        C2[Container B]
    end

    subgraph LogChain_Core [src/log.py & src/chain.py]
        S[Background Scheduler] -->|Every 60s| Poll[Fetch 1m Log Slice]
        Poll --> Hash[Generate SHA-256 Hash]
        Hash --> Combine{Combine with Prev Hash}
        Combine --> Link[Create Cryptographic Link]
    end

    subgraph Storage [Persistent Data]
        DB[(JSON/SQLite Store)]
    end

    subgraph Web_Interface [src/app.py]
        UI[Flask Dashboard]
        Theme[Gruvbox CSS]
    end

    %% Connections
    D --- C1
    D --- C2
    Poll -.->|Read| D
    Link -->|Save Link + Logs| DB
    UI -->|Query| DB
    Theme --> UI
    
    %% Styling
    style Link fill:#b8bb26,stroke:#3c3836,color:#282828
    style Hash fill:#fabd2f,stroke:#3c3836,color:#282828
    style UI fill:#8ec07c,stroke:#3c3836,color:#282828
    style D fill:#83a598,stroke:#3c3836,color:#fff
```


## Quick Start

Edit the docker-compose.yml file to your liking. You can configure log levels, alerting rules, and storage paths. To test and startup, you can use:
```yaml
services:
  logchain-web:
    build: .
    ports:
      - "5000:5000"
    container_name: logchain_web
    restart: unless-stopped
```

Ensure you have Docker (and Docker Compose) installed. Run:
```sh
docker-compose up --build
```

Once the container is running, LogChain will begin indexing existing logs and watching for new events. You can view the web interface at http://localhost:5000. Run `docker-compose down` when finished.


## Contributing

See [CONTRIBUTING](CONTRIBUTING).


## License

This project is licensed under the [MIT License](LICENSE).


## AI Disclosure

AI assistance was used in styling the webpages **only**. Nothing else was *vibe coded*.
