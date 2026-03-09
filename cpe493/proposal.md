# CPE493 Project Proposal

## PROMPT

Write a ONE page proposal for the term project that includes the following:
1. Names of team members (up to 3)
2. Title
3. Objective of the Project
4. How you will achieve that objective
5. Why is that important (i.e., value/impact)?

As discussed in class, this can range from a survey/critical review of existing techniques to hands-on implementations.


## SUBMISSION

### Historian Tampering Detector

CPE493 Project Proposal - Austin Driggs and Caleb Edwards - 2026-02-23

### Objective of the Project

The objective is to design and implement a "Secure by Design" logging and alerting system for a single-board server (Raspberry Pi/SBC) running Docker. The project aims to prevent "log scrubbing" by attackers who gain root access. By cryptographically signing Docker container logs in real-time and triggering immediate external notifications for suspicious activity, we ensure an immutable audit trail and real-time response.

### Achieving the Objective

We will deploy a local Docker environment on a single board and implement a monitoring agent (using Python or Go) that hooks into the Docker socket to ingest logs. As each log line is generated, the agent will:
1. Append it to a cryptographically chained file (where each entry includes the hash of the previous line).
2. Monitor for "High-Priority" keywords (e.g., "authentication failed," "root," "rm -rf").
3. Trigger an immediate notification via a pub-sub notification if a signature mismatch or a high-priority event is detected.

Evaluation will include a "red-team" test where we attempt to delete log lines and measure how quickly the system detects the break in the cryptographic chain and sends an alert.

### Value and Impact of the Project

In modern homelabs and industrial edge computing, Docker containers are often the primary targets for exploitation. If an attacker gains access, their first step is usually to wipe the logs to hide their tracks. This project provides a low-overhead, self-hosted security layer that ensures "observability-as-security," giving administrators a reliable, tamper-evident record of everything that happens inside their containerized environment.
