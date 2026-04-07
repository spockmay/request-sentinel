import json
from datetime import datetime, timezone
from .db import db


class RequestLog(db.Model):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(2048), nullable=False)
    query_string = db.Column(db.Text, nullable=True)
    remote_addr = db.Column(db.String(45), nullable=True)  # supports IPv6
    user_agent = db.Column(db.Text, nullable=True)
    request_body = db.Column(db.Text, nullable=True)  # raw JSON body as string
    status_code = db.Column(db.Integer, nullable=True)
    response_time_ms = db.Column(db.Float, nullable=True)

    def to_dict(self):
        # Attempt to deserialize body back to JSON for cleaner API responses
        body = self.request_body
        try:
            body = json.loads(body) if body else None
        except (json.JSONDecodeError, TypeError):
            pass  # leave as raw string if not valid JSON

        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "method": self.method,
            "path": self.path,
            "query_string": self.query_string,
            "remote_addr": self.remote_addr,
            "user_agent": self.user_agent,
            "request_body": body,
            "status_code": self.status_code,
            "response_time_ms": self.response_time_ms,
        }

    def __repr__(self):
        return f"<RequestLog {self.method} {self.path} {self.status_code}>"
