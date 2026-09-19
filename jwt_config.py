import os
from datetime import timedelta

from botocore.exceptions import ClientError
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
)

from configuration import Authenticator, DynamoDBUserRepository


def create_app(monitoring=None):
    app = Flask(__name__)

    # Keep token lifetimes and secrets configurable for each deployment.

    app.config["JSON_SORT_KEYS"] = False
    jwt_secret = os.environ.get("JWT_SECRET_KEY")


    if not jwt_secret and os.environ.get("APP_ENV", "development") == "production":
        raise RuntimeError("JWT_SECRET_KEY must be configured in production")
    app.config["JWT_SECRET_KEY"] = jwt_secret or "development-secret-change-me-32-bytes"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = os.environ.get("APP_ENV") == "production"
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_MINUTES", "15"))
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        days=int(os.environ.get("JWT_REFRESH_DAYS", "30"))
    )

    app.config["JWT_DECODE_LEEWAY"] = 5

    jwt = JWTManager(app)

    table_name = os.environ.get("DYNAMODB_TABLE", "users")
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    # Construct the repository once so every route reuses the same service.
    repository = DynamoDBUserRepository(table_name, region_name)
    auth_system = Authenticator(repository)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad request", "error": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"message": "Unauthorized"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Route not found"}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"message": "Internal server error"}), 500

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "service": "jwt-api"}), 200

    @app.route("/api/v1/auth/register", methods=["POST"])
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return jsonify({"message": "username and password are required"}), 400

        try:
            auth_system.create_user(username, password)

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return jsonify({
                "message": "User registered successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": int(app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()),
            }), 200
        except ClientError:
            return jsonify({"message": "Failed to connect to DynamoDB"}), 500

    @app.route("/api/v1/auth/login", methods=["POST"])
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return jsonify({"message": "username and password are required"}), 400

        try:
            success, message = auth_system.authenticate(username, password)

            if success:

                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)


                response = jsonify({
                    "message": message,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "Bearer",
                    "expires_in": int(app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()),
                })


                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)

                if monitoring is not None:
                    monitoring.safely_write_log(
                        f"Successful login for user: {username}", level="INFO"
                    )
                    monitoring.safely_record("SuccessfulLogins")
                    monitoring.safely_notify(
                        subject="Security Alert: Successful Login",
                        message=f"The user '{username}' logged in successfully.",
                    )

                return response, 200

            if monitoring is not None:
                monitoring.safely_write_log(
                    f"Failed login attempt for user: {username}", level="WARNING"
                )
                monitoring.safely_record("FailedLogins")
                monitoring.safely_notify(
                    subject="Security Alert: Failed Login Attempt",
                    message=f"A failed login attempt was detected for username: '{username}'.",
                )

            status_code = 403 if "locked" in message.lower() else 401
            return jsonify({"message": message}), status_code

        except ClientError:
            return jsonify({"message": "Failed to connect to DynamoDB"}), 500

    @app.route("/api/v1/auth/refresh", methods=["POST"])
    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        """Exchange a refresh token for a rotated access/refresh token pair."""
        current_user = get_jwt_identity()
        # Refreshing does not query DynamoDB, keeping this frequent path fast.
        access_token = create_access_token(identity=current_user)
        refresh_token = create_refresh_token(identity=current_user)
        response = jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": int(app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()),
        })
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200

    @app.route("/api/v1/auth/me", methods=["GET"])
    @app.route("/me", methods=["GET"])
    @jwt_required()
    def get_profile():
        current_user = get_jwt_identity()
        return jsonify({
            "logged_in_as": current_user,
            "status": "Access confirmed",
            "database": "DynamoDB",
            "protected": True

        }), 200

    @app.route("/protected_token", methods=["GET"])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify({
            "logged_in_as": current_user,
            "status": "Access confirmed",
            "database": "DynamoDB",
            "protected": True,
        }), 200

    return app