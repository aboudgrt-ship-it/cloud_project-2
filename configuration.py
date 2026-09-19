import os
import time
from typing import Optional, Tuple
from datetime import datetime , timezone

import bcrypt
import boto3
from botocore.exceptions import ClientError

MAX_ATTEMPTS = 5
LOCKOUT_DURATION_SECONDS = 900  # 15 minutes

class DynamoDBUserRepository:
    """Store and retrieve user authentication data in DynamoDB."""

    def __init__(self, table_name: str, region_name: str) -> None:
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = dynamodb.Table(table_name)

    def save_user(self, username: str, password_hash: bytes) -> None:
        """Create a new user with initial security fields."""
        self.table.put_item(
            Item={
                "username": username,
                "password_hash": password_hash.decode("utf-8"),
                "failed_attempts": 0,
                "lockout_until": 0,
            },
            ConditionExpression="attribute_not_exists(username)",
        )

    def get_user_data(self, username: str) -> Optional[dict]:
        """Fetch all user data from DynamoDB."""
        response = self.table.get_item(Key={"username": username})
        return response.get("Item")

    def increment_failed_attempts(self, username: str) -> int:
        """Increment failed attempts and set lockout if threshold reached."""
        response = self.table.update_item(
            Key={"username": username},
            UpdateExpression="SET failed_attempts = failed_attempts + :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW"
        )
        attempts = int(response["Attributes"]["failed_attempts"])

        if attempts >= MAX_ATTEMPTS:
            lockout_time = int(time.time()) + LOCKOUT_DURATION_SECONDS
            self.table.update_item(
                Key={"username": username},
                UpdateExpression="SET lockout_until = :lt",
                ExpressionAttributeValues={":lt": lockout_time}
            )
        return attempts

    def reset_failed_attempts(self, username: str) -> None:
        """Reset failed attempts and lockout upon successful login."""
        self.table.update_item(
            Key={"username": username},
            UpdateExpression="SET failed_attempts = :zero, lockout_until = :zero",
            ExpressionAttributeValues={":zero": 0},
        )


class Authenticator:
    """Handle user registration and secure password verification."""

    def __init__(self, user_repository: DynamoDBUserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, username: str, password: str) -> None:
        """Validate input and hash password before saving."""
        username = username.strip()
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        password_hash = self.hash_password(password)
        self.user_repository.save_user(username, password_hash)

    @staticmethod
    def hash_password(password: str) -> bytes:
        """Generate a secure bcrypt  hash."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate a user with brute-force protection.
        Returns: (Success Boolean, Message String)
        """
        user_data = self.user_repository.get_user_data(username)

        if not user_data:
            return False, "Invalid username or password."

        # 1. Check if the account is currently locked
        current_time = int(time.time())
        lockout_until = int(user_data.get("lockout_until", 0))

        if lockout_until > current_time:
            wait_time = (lockout_until - current_time) // 60
            return False, f"Account locked. Try again in {max(1, wait_time)} minutes."

        # 2. Verify Password
        stored_hash = user_data.get("password_hash", "").encode("utf-8")
        try:
            password_matches = bcrypt.checkpw(password.encode("utf-8"), stored_hash)
        except (ValueError, TypeError):
            password_matches = False

        if password_matches:
            # Success: Reset attempts
            self.user_repository.reset_failed_attempts(username)
            return True, "Login successful."
        else:
            # Failure: Increment attempts and potentially lock
            attempts = self.user_repository.increment_failed_attempts(username)
            if attempts >= MAX_ATTEMPTS:
                return False, f"Too many failed attempts. Account locked for {LOCKOUT_DURATION_SECONDS // 60} minutes."
            return False, "Invalid username or password."

    def get_user_profile(self, username: str) -> Optional[dict]:
        """Retrieve non-sensitive user data."""
        user_data = self.user_repository.get_user_data(username)
        if not user_data:
            return None
        # Return only safe fields
        return {"username": user_data.get("username")}


def main() -> None:
    table_name = os.getenv("DYNAMODB_TABLE", "users")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    repository = DynamoDBUserRepository(table_name, region_name)
    authenticator = Authenticator(repository)

    action = input("Choose action (register/login): ").strip().lower()
    username = input("Username: ").strip()

    if action == "register":
        password = input("Password: ")
        try:
            authenticator.create_user(username, password)
            print("User registered successfully.")
        except Exception as e:
            print(f"Error: {e}")

    elif action == "login":
        password = input("Password: ")
        try:
            success, message = authenticator.authenticate(username, password)
            print(message)
        except ClientError as error:
            print(f"Database error: {error.response['Error']['Code']}")
    else:
        print("Invalid action.")


