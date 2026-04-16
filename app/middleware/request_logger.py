import json
import time
from flask import request, g
from ..models.db import db
from ..models.request_log import RequestLog


class RequestLoggerMiddleware:
    """Hooks into Flask's before/after request lifecycle to log all requests."""

    def __init__(self, app):
        self.app = app
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        g.start_time = time.perf_counter()

        # Capture raw body — must be done before the route handler consumes it
        try:
            body = request.get_data(as_text=True)
            # Normalize to compact JSON if valid, otherwise store raw
            g.request_body = json.dumps(json.loads(body)) if body else None
        except (json.JSONDecodeError, UnicodeDecodeError):
            g.request_body = body or None

    def _after_request(self, response):
        elapsed_ms = (time.perf_counter() - g.start_time) * 1000

        log_entry = RequestLog(
            method=request.method,
            path=request.path,
            query_string=request.query_string.decode("utf-8") or None,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            request_body=getattr(g, "request_body", None),
            status_code=response.status_code,
            response_time_ms=round(elapsed_ms, 3),
        )

        if log_entry.status_code == 401:
            # ignore unauthenticated requests
            return response

        if "ELB-HealthChecker" in log_entry.user_agent:
            # ignore AWS's load balancer health checks
            return response

        if "/logs" == log_entry.path:
            # ignore requests to view the latest log entries
            return response

        try:
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            self.app.logger.error(f"Failed to log request: {e}")

        return response
