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
)

from configuration import Authenticator, DynamoDBUserRepository


def create_app():
    app = Flask(__name__)

    # API configuration
    app.config["JSON_SORT_KEYS"] = False
    jwt_secret = os.environ.get("JWT_SECRET_KEY")
    if not jwt_secret and os.environ.get("APP_ENV", "development") == "production":
        raise RuntimeError("JWT_SECRET_KEY must be configured in production")
    app.config["JWT_SECRET_KEY"] = jwt_secret or "development-secret-change-me-32-bytes"
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
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

    # One shared authentication service for all routes.
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
            return jsonify({"message": "User created successfully", "username": username}), 201
        except ValueError as error:
            return jsonify({"message": str(error)}), 400
        except ClientError as error:
            return jsonify({"message": "DynamoDB error", "error": str(error)}), 500

    @app.route("/api/v1/auth/login", methods=["POST"])
    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return jsonify({"message": "username and password are required"}), 400

        try:
            if auth_system.verify_user(username, password):
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                return jsonify({
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "Bearer",
                    "expires_in": int(app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()),
                }), 200

            return jsonify({"message": "Invalid username or password"}), 401
        except ClientError as error:
            return jsonify({"message": "Failed to connect to DynamoDB", "error": str(error)}), 500

    @app.route("/api/v1/auth/refresh", methods=["POST"])
    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        """Exchange a refresh token for a rotated access/refresh token pair."""
        current_user = get_jwt_identity()
        return jsonify({
            "access_token": create_access_token(identity=current_user),
            "refresh_token": create_refresh_token(identity=current_user),
            "token_type": "Bearer",
            "expires_in": int(app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()),
        }), 200

    @app.route("/api/v1/auth/me", methods=["GET"])
    @app.route("/me", methods=["GET"])
    @jwt_required()
    def get_profile():
        current_user = get_jwt_identity()
        return jsonify({
            "logged_in_as": current_user,
            "status": "Access confirmed",
            "database": "DynamoDB",
        }), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)