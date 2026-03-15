from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
            <style>
                body { background-color: #121212; color: #e0e0e0; font-family: sans-serif; padding: 40px; line-height: 1.6; }
                h1 { color: #00ffcc; }
                .container { max-width: 800px; margin: auto; }
            </style>
            <div class="container">
                <h1>LogChain: A Lightweight and Secure Docker Historian</h1>
                <p>LogChain is a lightweight security tool that provides <strong>tamper-evident logging</strong> for Docker environments. 
                It continuously monitors container logs, cryptographically chains each log entry to preserve an <strong>immutable record</strong>, 
                and alerts administrators when suspicious activity or log tampering is detected.</p>
                
                <p>The system is designed for homelabs, edge devices, and small servers where maintaining trustworthy logs is critical 
                but ease of use and flexibility is desired.</p>
            </div>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)