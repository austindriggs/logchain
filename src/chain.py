import hashlib
import datetime
import json

class LogChain:
    def __init__(self):
        # The 'Genesis' hash for the very first log entry
        self.last_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    # generates a hash and returns it as a string
    def generate_hash(self, timestamp, container_name, container_logs):
        block_string = f"{self.last_hash}{timestamp}{container_name}{container_logs}"
        hash_object = hashlib.sha256(block_string.encode('utf-8'))

        return hash_object.hexdigest()
    
    # create a new block and return it as a dictionary
    def create_block(self, container_name, container_logs):
        timestamp = datetime.datetime.now().isoformat()
        new_hash = self.generate_hash(timestamp, container_name, container_logs)
        
        block = {
            "timestamp": timestamp,
            "container": container_name,
            "logs": container_logs,
            "last_hash": self.last_hash,
            "new_hash": new_hash
        }
        self.last_hash = new_hash
        
        return block






    def verify_chain(self, entries):
        check_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        
        for entry in entries:
            # Re-calculate what the hash SHOULD be
            expected = self.generate_hash(entry['container'], entry['logs'], entry['timestamp'])
            
            if entry['new_hash'] != expected or entry['last_hash'] != check_hash:
                return False, entry
            
            check_hash = entry['hash']
            
        return True, None

    
    


    def write_block(self, entry):
        filepath = "/app/data/logchain.json"
        data = []
        
        # Load existing data if file exists
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        
        data.append(entry)
        
        # Write back to file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True

    def read_block(self, hash_value):
        filepath = "/app/data/logchain.json"
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            data = json.load(f)
            for entry in data:
                if entry.get('hash') == hash_value:
                    return entry
        return None

    def export_chain(self, entries, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(entries, f, indent=4)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    def import_chain(self, filename):
        if not os.path.exists(filename):
            return []

        with open(filename, 'r') as f:
            data = json.load(f)
            if data:
                # Update the state of the class to the end of the imported chain
                self.last_hash = data[-1]['hash']
            return data

