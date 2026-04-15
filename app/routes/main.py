from flask import Blueprint, jsonify, request, Flask
from ..models.request_log import RequestLog
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# In a real app, users should be stored in the database
users = {"admin": generate_password_hash("secret_password")}

main_bp = Blueprint("main", __name__)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(
        users.get(username, ""), password
    ):
        return username


@main_bp.route("/", methods=["GET", "POST"])
@auth.login_required
def index():
    return jsonify({"status": "ok", "service": "request-sentinel"})


@main_bp.route("/test", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@auth.login_required
def test_endpoint():
    """Catch-all test endpoint for verifying request logging."""
    return jsonify(
        {
            "status": "ok",
            "method": request.method,
            "body": request.get_json(silent=True),
        }
    )


@main_bp.route("/logs")
@auth.login_required
def get_logs():
    """Return the 100 most recent request logs."""
    logs = (
        RequestLog.query.order_by(RequestLog.timestamp.desc()).limit(100).all()
    )
    return jsonify([log.to_dict() for log in logs])


# This will handle any /* URL call instead of throwing a 404
@main_bp.route("/<path:url>", methods=["GET", "POST"])
@auth.login_required
def wildcard(url):
    return jsonify({"status": "ok", "service": "request-sentinel"})
