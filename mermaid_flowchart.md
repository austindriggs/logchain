flowchart TD

%% DATA SOURCES
A["Docker Containers
(Simulated Solar Panel, etc)"]


%% LOG COLLECTION
C[log.py 
Get Container Logs]

%% PROCESSING
D["Extract New Logs (Scheduled and new only)"]
E["solar_alerts.py
(Test  to Detect Faults)"]
F["alert.py 
(Send ntfy Notification)"]

%% BLOCKCHAIN
G["Create Block
(timestamp, logs, and prev_hash)"]
H["Hash Block with (SHA256)"]
I[Append to Chain]
J["Save chain.json
(Log the Chain)"]

%% UI + API

L["Web UI 
(Block Viewer and Alert Interface)"]

%% FLOW CONNECTIONS
A --> C
C --> D
D --> G
G --> H
H --> I
I --> J

%% ALERT FLOW
I --> E
E --> F

%% UI FLOW
I --> L