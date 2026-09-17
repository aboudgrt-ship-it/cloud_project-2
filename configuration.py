import os
from typing import Optional

import bcrypt
import boto3
from botocore.exceptions import ClientError


class DynamoDBUserRepository:
    """Store and retrieve user password hashes in DynamoDB."""

    def __init__(self, table_name: str, region_name: str) -> None:
        # We create a DynamoDB table resource once so the app can reuse it.
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = dynamodb.Table(table_name)

    def save_password_hash(self, username: str, password_hash: bytes) -> None:
        # DynamoDB stores values as strings, numbers, or JSON-like objects.
        # Because raw bytes are not supported, we convert the hash to text before saving.
        self.table.put_item(
            Item={
                "username": username,
                "password_hash": password_hash.decode("utf-8"),
            }
        )

    def get_password_hash(self, username: str) -> Optional[bytes]:
        # If the user does not exist, DynamoDB returns no item.
        response = self.table.get_item(Key={"username": username})
        item = response.get("Item")

        if item is None:
            return None

        stored_hash = item.get("password_hash")
        if stored_hash is None:
            return None

        return stored_hash.encode("utf-8")


class Authenticator:
    """Handle user registration and password verification."""

    def __init__(self, user_repository: DynamoDBUserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, username: str, password: str) -> None:
        # It is better to validate input before saving to avoid blank usernames.
        username = username.strip()
        if not username:
            raise ValueError("Username cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")

        password_hash = self.hash_password(password)
        self.user_repository.save_password_hash(username, password_hash)

    @staticmethod
    def hash_password(password: str) -> bytes:
        # bcrypt automatically adds a random salt, so two identical passwords get different hashes.
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def get_stored_password_hash(self, username: str) -> Optional[bytes]:
        return self.user_repository.get_password_hash(username)

    def verify_user(self, username: str, password: str) -> bool:
        stored_password_hash = self.get_stored_password_hash(username)

        if stored_password_hash is None:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), stored_password_hash)


def main() -> None:
    # The table name and region should come from environment variables for flexibility and security.
    table_name = os.getenv("DYNAMODB_TABLE", "users")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    repository = DynamoDBUserRepository(table_name, region_name)
    authenticator = Authenticator(repository)

    username = input("Create a username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    try:
        authenticator.create_user(username, input("Create a password: "))
    except ClientError as error:
        print(f"Could not save user: {error.response['Error']['Code']}")
        return
    except ValueError as error:
        print(error)
        return

    for _ in range(3):
        password = input("Enter your password: ")
        try:
            if authenticator.verify_user(username, password):
                print("Login successful.")
                return
        except ClientError as error:
            print(f"Could not read user: {error.response['Error']['Code']}")
            return

        print("Incorrect password.")

    print("Too many failed attempts. Please try again later.")


