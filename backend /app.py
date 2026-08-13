from flask import Flask, jsonify
from flask_cors import CORS

from database import initialize_database
from auth import auth

app = Flask(__name__)
// secret key used for secure login sessions.
//replace this with a strong secret in a real deployment.
app.config["SECRET_KEY"] = "change-this-secret-key"

CORS(app, support_credentials=True)

// initialize database when the application starts
initialize_database()

//Register authentication routes
app.register_blueprint(auth)

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


