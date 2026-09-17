import os
from typing import Optional

import bcrypt
import boto3
from botocore.exceptions import ClientError


class DynamoDBUserRepository:
    """Store and retrieve user password hashes in DynamoDB."""

    def __init__(self, table_name: str, region_name: str) -> None:
        # Reuse one DynamoDB table resource for all repository operations.
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = dynamodb.Table(table_name)

    def save_password_hash(self, username: str, password_hash: bytes) -> None:
        # DynamoDB does not store raw password-hash bytes, so save the hash as text.
        self.table.put_item(
            Item={
                "username": username,
                "password_hash": password_hash.decode("utf-8"),
            }
        )

    def get_password_hash(self, username: str) -> Optional[bytes]:
        # A missing item means the username has not been registered.
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
        # Validate input before hashing or writing to DynamoDB.
        username = username.strip()
        if not username:
            raise ValueError("Username cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")

        password_hash = self.hash_password(password)
        self.user_repository.save_password_hash(username, password_hash)

    @staticmethod
    def hash_password(password: str) -> bytes:
        # bcrypt adds a random salt, so identical passwords produce different hashes.
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def get_stored_password_hash(self, username: str) -> Optional[bytes]:
        return self.user_repository.get_password_hash(username)

    def verify_user(self, username: str, password: str) -> bool:
        stored_password_hash = self.get_stored_password_hash(username)

        if stored_password_hash is None:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), stored_password_hash)


def main() -> None:
    # Keep deployment-specific AWS settings outside the source code.
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


