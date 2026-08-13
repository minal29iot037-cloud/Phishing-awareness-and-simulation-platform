from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection

auth = Blueprint("auth", __name__)


@auth.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must contain at least 8 characters"
        }), 400

    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, password_hash, "user")
        )
        connection.commit()

    except Exception:
        connection.close()
        return jsonify({
            "error": "Email is already registered"
        }), 409

    connection.close()

    return jsonify({
        "message": "Registration successful"
    }), 201


@auth.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, name, email, password_hash, role
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if user is None or not check_password_hash(
        user["password_hash"], password
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    session["user_id"] = user["id"]
    session["role"] = user["role"]

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })


@auth.route("/api/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "message": "Logout successful"
    })


@auth.route("/api/me", methods=["GET"])
def current_user():
    if "user_id" not in session:
        return jsonify({
            "error": "Authentication required"
        }), 401

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, name, email, role
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    connection.close()

    if user is None:
        session.clear()
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "user": dict(user)
    })
