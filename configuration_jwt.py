import os
import boto3
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from botocore.exceptions import ClientError

from authurization import DynamoDBUserRepository, Authenticator

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret-aws-key")
jwt = JWTManager(app)


TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "users")
REGION_NAME = os.environ.get("AWS_REGION", "us-east-1")

repository = DynamoDBUserRepository(TABLE_NAME, REGION_NAME)
auth_system = Authenticator(repository)



@app.route("/register", methods=["POST"])
def register():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "username and password are requierd"}), 400

    try:
        auth_system.create_user(username, password)
        return jsonify({"msg": f"user created {username}"}), 201
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
    
        if auth_system.verify_user(username, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "wrong occured while authourization "}), 401
            
    except ClientError as e:
        return jsonify({"error": "failed to connect to AWS DynamoDB"}), 500


@app.route("/me", methods=["GET"])
@jwt_required()
def get_profile():

    current_user = get_jwt_identity()
    return jsonify({
        "logged_in_as": current_user,
        "status": "Access confirmed",
        "database": "DynamoDB"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
