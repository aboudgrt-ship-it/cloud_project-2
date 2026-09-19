import importlib
import sys
import unittest
from unittest.mock import Mock, patch

from configuration import Authenticator, DynamoDBUserRepository
from jwt_config import create_app


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.repository = Mock()
        self.monitoring = Mock()
        self.app_patch = patch(
            "jwt_config.DynamoDBUserRepository",
            return_value=self.repository,
        )
        self.app_patch.start()
        self.addCleanup(self.app_patch.stop)

        self.app = create_app(monitoring=self.monitoring)
        self.app.config.update(
            TESTING=True,
            JWT_SECRET_KEY="test-secret-key-with-at-least-32-bytes",
        )
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_login_requires_credentials(self):
        response = self.client.post("/login", json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["message"],
            "username and password are required",
        )

    def test_successful_login_returns_tokens_and_records_monitoring(self):
        password_hash = Authenticator.hash_password("correct-password")
        self.repository.get_user_data.return_value = {
            "username": "alice",
            "password_hash": password_hash.decode("utf-8"),
            "failed_attempts": 0,
            "lockout_until": 0,
        }

        response = self.client.post(
            "/api/v1/auth/login",
            json={"username": "alice", "password": "correct-password"},
        )
        payload = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["token_type"], "Bearer")
        self.assertIn("access_token", payload)
        self.assertIn("refresh_token", payload)
        self.repository.reset_failed_attempts.assert_called_once_with("alice")
        self.monitoring.safely_record.assert_called_once_with("SuccessfulLogins")
        self.monitoring.safely_write_log.assert_called_once()
        self.monitoring.safely_notify.assert_called_once()

    def test_failed_login_returns_unauthorized(self):
        self.repository.get_user_data.return_value = {
            "username": "alice",
            "password_hash": Authenticator.hash_password("correct-password").decode(
                "utf-8"
            ),
            "failed_attempts": 0,
            "lockout_until": 0,
        }
        self.repository.increment_failed_attempts.return_value = 1

        response = self.client.post(
            "/login",
            json={"username": "alice", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Invalid username or password.")
        self.monitoring.safely_record.assert_called_once_with("FailedLogins")

    def test_protected_endpoint_requires_jwt(self):
        response = self.client.get("/me")

        self.assertEqual(response.status_code, 401)

    def test_expected_route_aliases_are_registered_once(self):
        routes = {}
        for rule in self.app.url_map.iter_rules():
            routes.setdefault(rule.endpoint, []).append(rule.rule)

        self.assertCountEqual(routes["login"], ["/login", "/api/v1/auth/login"])
        self.assertCountEqual(routes["register"], ["/register", "/api/v1/auth/register"])
        self.assertCountEqual(routes["refresh"], ["/refresh", "/api/v1/auth/refresh"])


class DynamoDBRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repository = DynamoDBUserRepository.__new__(DynamoDBUserRepository)
        self.repository.table = Mock()

    def test_save_user_does_not_overwrite_existing_user(self):
        self.repository.save_user("alice", b"hashed-password")

        call = self.repository.table.put_item.call_args.kwargs
        self.assertEqual(call["ConditionExpression"], "attribute_not_exists(username)")

    def test_reset_failed_attempts_uses_valid_dynamodb_arguments(self):
        self.repository.reset_failed_attempts("alice")

        call = self.repository.table.update_item.call_args.kwargs
        self.assertNotIn("timezone", call)
        self.assertNotIn("time", call)
        self.assertEqual(call["ExpressionAttributeValues"], {":zero": 0})


class ApplicationStartupTests(unittest.TestCase):
    def test_main_creates_flask_application_without_aws_calls(self):
        mock_resource = Mock()
        mock_resource.Table.return_value = Mock()

        with patch("boto3.resource", return_value=mock_resource), patch(
            "boto3.client", return_value=Mock()
        ):
            sys.modules.pop("main", None)
            main_module = importlib.import_module("main")

        self.assertIsNotNone(main_module.app)
        self.assertEqual(main_module.app.url_map._rules_by_endpoint["login"].__len__(), 2)
        sys.modules.pop("main", None)


if __name__ == "__main__":
    unittest.main()