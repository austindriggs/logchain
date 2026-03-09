from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome to My Simple Flask Website!</h1>'

@app.route('/about')
def about():
    return '<h1>About Page</h1><p>This is a simple website built with Flask.</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)