from flask import Flask, request, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

# Configuration (in a production system, use environment variables securely)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "db")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "usersdb")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)


# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )
    return conn


# Connect to Redis
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/")
def index():
    return "User Service is up and running!"


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Save to PostgreSQL
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Cache the username in Redis
    cache.set(f"user:{user_id}", username)

    return jsonify({"id": user_id, "username": username}), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # Try to fetch from Redis first
    username = cache.get(f"user:{user_id}")
    if username:
        return jsonify({"id": user_id, "username": username, "cached": True})

    # If not in cache, fetch from PostgreSQL
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        username = row[0]
        # Cache the result for future requests
        cache.set(f"user:{user_id}", username)
        return jsonify({"id": user_id, "username": username, "cached": False})
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    # For development only; use a proper WSGI server (e.g. gunicorn) in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
