import os
import boto3
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from botocore.exceptions import NoCredentialsError, ClientError



app = Flask(__name__)
app.config["jwt_secret_key"] , os.environ["fallback_dev", "jwt_secret_key"]

jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username" , None)
    password = request.json.get("password" , None)

