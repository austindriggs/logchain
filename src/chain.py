# chain.py
# builds a simple hash chain of container logs using SHA256

##############################################################################
# IMPORTS
##############################################################################

import datetime
import hashlib
import log  # uses your existing log.py

##############################################################################
# GLOBAL CHAIN STORAGE
##############################################################################

chain = []

##############################################################################
# HELPER FUNCTIONS
##############################################################################

def sha256_text(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    return hashlib.sha256(text).hexdigest()


def get_latest_hash():
    if not chain:
        return "0" * 64  # genesis previous hash
    return chain[-1]["block_hash"]

##############################################################################
# CORE FUNCTION: ADD BLOCK
##############################################################################

def add_block():
    global chain

    logs = log.get_hashed_logs()
    timestamp = datetime.datetime.utcnow().isoformat()

    previous_hash = get_latest_hash()

    block_data = {
        "timestamp": timestamp,
        "logs": logs,
        "previous_hash": previous_hash
    }

    # stringify block content for hashing
    block_string = f"{timestamp}{logs}{previous_hash}"
    block_hash = sha256_text(block_string)

    block = {
        **block_data,
        "block_hash": block_hash
    }

    chain.append(block)

    return block

##############################################################################
# VALIDATION FUNCTION
##############################################################################

def validate_chain():
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        # check previous hash link
        if current["previous_hash"] != previous["block_hash"]:
            return False

        # recompute hash
        block_string = f"{current['timestamp']}{current['logs']}{current['previous_hash']}"
        recalculated_hash = sha256_text(block_string)

        if current["block_hash"] != recalculated_hash:
            return False

    return True

##############################################################################
# ACCESS FUNCTION
##############################################################################

def get_chain():
    return chain