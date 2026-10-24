import os
import time
import redis
from flask import Flask, jsonify

app = Flask(__name__)

# Connects to a service called "redis" -- this only works if the container
# running this app can resolve the hostname "redis". Think about why, based
# on what you learned about container networking.
redis_host = os.environ.get("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from inside the container!",
        "hostname": os.environ.get("HOSTNAME", "unknown"),
    })


@app.route("/count")
def count():
    try:
        visits = r.incr("visits")
        return jsonify({"visits": visits})
    except redis.exceptions.ConnectionError as e:
        return jsonify({"error": f"Could not reach redis: {str(e)}"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": time.time()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
