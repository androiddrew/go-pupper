from flask import Flask, jsonify

# app
from .stats import get_stats

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/api/stats")
def stats():
    """Provides CPU, Memory, and Disk utilization of the current host"""
    stats = get_stats()
    return jsonify(stats)
