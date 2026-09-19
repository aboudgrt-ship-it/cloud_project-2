import bcrypt
import os
import boto3
from botocore.exceptions import ClientError


attempets = 0 

class DynamoDBUserRepository:
    def __init__(self, table_name: str, region_name: str) -> None:
        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = dynamodb.Table(table_name)

    def save_password_hash(self, username: str, password_hash: bytes) -> None:
        self.table.put_item(
            Item={
                "username": username,
                "password_hash": password_hash.decode("utf-8"),
            }
        )

    def get_password_hash(self, username: str) -> bytes | None:
        response = self.table.get_item(Key={"username": username})
        item = response.get("Item")
        if item is None:
            return None
        return item["password_hash"].encode("utf-8")


class Authenticator:
    def __init__(self, user_repository: DynamoDBUserRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, username: str, password: str) -> None:
        password_hash = self.hash_password(password)
        self.user_repository.save_password_hash(username, password_hash)

    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def get_stored_password_hash(self, username: str) -> bytes | None:
        return self.user_repository.get_password_hash(username)
        if password_hash != stored_password_hash:
            raise ValueError("Incorrect password")
            
    def verify_user(self, username: str, password: str) -> bool:
        stored_password_hash = self.get_stored_password_hash(username)

        if stored_password_hash is None:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), stored_password_hash)


def main() -> None:
    table_name = os.getenv("DYNAMODB_TABLE", "users")
    region_name = os.getenv("AWS_REGION", "us-east-1")
    repository = DynamoDBUserRepository(table_name, region_name)
    authenticator = Authenticator(repository)
    username = input("Create a username: ")
    try:
        authenticator.create_user(username, input("Create a password: "))
    except ClientError as error:
        print(f"Could not save user: {error.response['Error']['Code']}")
        return

    for attempt in range(3):
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


if __name__ == "__main__":
    main()
