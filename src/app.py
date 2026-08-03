"""
app.py
------
A small Flask API exposing User functions over HTTP. Runs entirely
on your own machine (http://localhost:5000) -- nothing here talks
to any external server.

Requires: pip install flask flask-cors

Run with (from inside the src/ folder):
    python app.py
"""

from flask import Flask, request, jsonify

from User import user_repository as users

app = Flask(__name__)

# ---------------------------------------------------------------
# CORS: since your HTML/JS files are opened from a different
# origin (a file:// path or a different localhost port) than
# this Flask server, the browser blocks the request by default.
# flask-cors turns that blocking off for local development.
# ---------------------------------------------------------------
from flask_cors import CORS
CORS(app)


@app.route("/api/signup", methods=["POST"])
def signup():
    """
    Expects JSON like:
    {
        "firstName": "Hetal",
        "lastName": "Kumar",
        "username": "hetalk",
        "email": "hetal@example.com",
        "password": "secret123"
    }
    (age is intentionally not accepted -- it's computed from dob, not stored)
    """
    data = request.get_json()

    required = ["firstName", "username", "email", "password"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if users.get_user_by_username(data["username"]):
        return jsonify({"error": "Username already taken"}), 409

    new_id = users.create_user(
        first_name=data["firstName"],
        last_name=data["lastName"],
        username=data["username"],
        email=data["email"],
        password=data["password"],
        phone_number=data.get("phoneNumber"),
        dob=data.get("dob"),
    )

    return jsonify({"message": "Account created", "userId": new_id}), 201


@app.route("/api/login", methods=["POST"])
def login():
    """
    Expects JSON like:
    { "username": "hetalk", "password": "secret123" }
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users.authenticate_user(username, password)

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    user.pop("password_hash", None)
    return jsonify({"message": "Login successful", "user": user}), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    user.pop("password_hash", None)
    return jsonify(user), 200


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    users.update_user(user_id, **data)
    return jsonify({"message": "User updated"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)