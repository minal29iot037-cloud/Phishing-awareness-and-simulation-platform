from flask import Flask, jsonify
from flask_cors import CORS

from database import initialize_database

app = Flask(__name__)
CORS(app)

// initialize database when the application starts
initialize_database()

@app.route("/")
def home():
  return jsonify({ 
    "message": "Phishing Awareness and Simulation Platform API",
    "status": "running"
  } )

@app.route("/api/health")
def health():
  return jsonify({
    "status": "healthy"
    "database": "connected"
  })

if __name__ == "__main__":
  app.run(debug=True)


