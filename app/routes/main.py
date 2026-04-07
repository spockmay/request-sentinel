from flask import Blueprint, jsonify, request
from ..models.request_log import RequestLog

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    return jsonify({"status": "ok", "service": "request-sentinel"})


@main_bp.route("/test", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
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
def get_logs():
    """Return the 100 most recent request logs."""
    logs = (
        RequestLog.query.order_by(RequestLog.timestamp.desc()).limit(100).all()
    )
    return jsonify([log.to_dict() for log in logs])


# This will handle any /* URL call instead of throwing a 404
@main_bp.route("/<path:url>", methods=["GET", "POST"])
def wildcard():
    return jsonify({"status": "ok", "service": "request-sentinel"})
