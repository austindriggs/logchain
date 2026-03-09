from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
            <style>
                body { background-color: #121212; color: #e0e0e0; font-family: sans-serif; padding: 40px; }
                h1 { color: #00ffcc; }
            </style>
            <h1>LogChain: A Tamper-Evident Docker Logging System!</h1>
            <p>LogChain is a lightweight security tool that provides tamper-evident logging for Docker environments. It continuously monitors container logs, cryptographically chains each log entry using SHA-256, and alerts administrators when suspicious activity or log tampering is detected.</p>
            <p>The system is designed for homelabs, edge devices, and small servers where maintaining trustworthy logs is critical but traditional SIEM infrastructure is too heavy.</p>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)