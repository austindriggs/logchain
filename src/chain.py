# chain.py
# builds a simple hash chain of container logs using SHA256

##############################################################################
# IMPORTS
##############################################################################

import datetime
import hashlib
import log
import json
import os

##############################################################################
# GLOBAL CHAIN STORAGE
##############################################################################

chain = []
last_logs = {}
CHAIN_FILE = os.path.join(os.path.dirname(__file__), "chain.json")

##############################################################################
# HELPER FUNCTIONS
##############################################################################

def sha256_text(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    return hashlib.sha256(text).hexdigest()


def get_latest_hash():
    if not chain:
        return "0" * 64
    return chain[-1]["block_hash"]


def serialize_block_data(timestamp, logs, previous_hash):
    """Ensure consistent hashing (VERY IMPORTANT)"""
    return json.dumps({
        "timestamp": timestamp,
        "logs": logs,
        "previous_hash": previous_hash
    }, sort_keys=True)


def save_chain():
    try:
        with open(CHAIN_FILE, "w") as f:
            json.dump(chain, f, indent=2)
    except Exception as e:
        print(f"Error saving chain: {e}")


def load_chain():
    global chain

    if not os.path.exists(CHAIN_FILE):
        chain = []
        return

    try:
        with open(CHAIN_FILE, "r") as f:
            chain = json.load(f)
    except Exception as e:
        print(f"Error loading chain: {e}")
        chain = []

##############################################################################
# CORE FUNCTION: ADD BLOCK
##############################################################################

def add_block():
    global chain, last_logs

    logs = log.get_logs()
    new_logs = {}

    for container, text in logs.items():
        prev = last_logs.get(container, "")

        # get only new portion
        if text.startswith(prev):
            diff = text[len(prev):]
        else:
            # fallback if logs rotated or changed
            diff = text

        new_logs[container] = diff

        # update stored logs
        last_logs[container] = text

    # optional: skip empty blocks
    if all(v.strip() == "" for v in new_logs.values()):
        return

    timestamp = datetime.datetime.utcnow().isoformat()
    previous_hash = get_latest_hash()

    # deterministic serialization (USE new_logs!)
    block_string = serialize_block_data(timestamp, new_logs, previous_hash)
    block_hash = sha256_text(block_string)

    block = {
        "timestamp": timestamp,
        "logs": new_logs,
        "previous_hash": previous_hash,
        "block_hash": block_hash
    }

    chain.append(block)
    save_chain()

    return block

##############################################################################
# VALIDATION FUNCTION
##############################################################################

def validate_chain():
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        if current["previous_hash"] != previous["block_hash"]:
            return False

        block_string = serialize_block_data(
            current["timestamp"],
            current["logs"],
            current["previous_hash"]
        )

        recalculated_hash = sha256_text(block_string)

        if current["block_hash"] != recalculated_hash:
            return False

    return True

##############################################################################
# ACCESS FUNCTION
##############################################################################

def get_chain():
    return chain

##############################################################################
# INIT
##############################################################################

load_chain()