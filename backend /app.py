from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
  })

if __name__ == "__main__":
  app.run(debug=True)
