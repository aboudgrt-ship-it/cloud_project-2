import os
import time

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from cloudwatch import CloudWatchIntegration
from jwt_config import create_app


app = create_app()
monitoring = CloudWatchIntegration(
    namespace=os.getenv("CLOUDWATCH_NAMESPACE", "JwtApi"),
)


@app.before_request
def start_request_timer() -> None:
    request.request_started_at = time.perf_counter()


@app.after_request
def record_request(response):
    duration_ms = round((time.perf_counter() - request.request_started_at) * 1000, 2)
    metric_name = "Http5xx" if response.status_code >= 500 else "HttpRequest"
    monitoring.safely_record(metric_name)
    monitoring.safely_write_log(
        f"{request.method} {request.path} {response.status_code} {duration_ms}ms",
        "ERROR" if response.status_code >= 500 else "INFO",
    )

    if response.status_code >= 500:
        monitoring.safely_notify(
            "JWT API server error",
            f"{request.method} {request.path} returned HTTP {response.status_code}",
        )
    return response


@app.route("/api/v1/aws/identity", methods=["GET"])
@jwt_required()
def aws_identity():
    """Show the IAM role or user used by boto3 for this application."""
    try:
        return jsonify(monitoring.caller_identity()), 200
    except Exception as error:
        monitoring.safely_notify("JWT API IAM check failed", str(error))
        return jsonify({"message": "Unable to verify AWS identity"}), 503


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )