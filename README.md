# Flask AWS JWT API

A Flask authentication API connected to AWS DynamoDB, AWS IAM credentials,
CloudWatch, and optional SNS notifications. The application uses bcrypt for
password hashing and Flask-JWT-Extended for short-lived access tokens and
long-lived refresh tokens.

## Project Files

The publishable application consists of four Python files:

- `configuration.py` - DynamoDB repository and bcrypt authentication service.
- `jwt_config.py` - Flask application factory and authentication endpoints.
- `cloudwatch.py` - CloudWatch metrics/logs, SNS notifications, and IAM identity checks.
- `main.py` - Application entry point that connects JWT routes to monitoring.

## Requirements

- Python 3.10 or newer.
- AWS credentials supplied by an IAM role, AWS profile, or environment.
- A DynamoDB table with `username` as its partition key.
- An IAM policy allowing the application to use DynamoDB, CloudWatch, CloudWatch Logs,
  SNS (if notifications are enabled), and STS `GetCallerIdentity`.

Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set these environment variables before running the application:

```bash
export APP_ENV=production
export JWT_SECRET_KEY="replace-with-a-long-random-secret"
export AWS_REGION=us-east-1
export DYNAMODB_TABLE=users
export JWT_ACCESS_MINUTES=15
export JWT_REFRESH_DAYS=30
export CLOUDWATCH_NAMESPACE=JwtApi
export CLOUDWATCH_LOG_GROUP=/jwt-api/application
export CLOUDWATCH_LOG_STREAM=flask
export SNS_TOPIC_ARN="arn:aws:sns:us-east-1:123456789012:jwt-api-alerts"
```

`SNS_TOPIC_ARN` is optional. If it is not set, notifications are skipped and
the application continues to operate. Never commit real credentials or secret
values to GitHub.

## Run

```bash
venv/bin/python main.py
```

The default address is `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Authentication | Purpose |
| --- | --- | --- | --- |
| `GET` | `/health` | None | Health check |
| `POST` | `/register` or `/api/v1/auth/register` | None | Create a DynamoDB user |
| `POST` | `/login` or `/api/v1/auth/login` | None | Return access and refresh tokens |
| `POST` | `/refresh` or `/api/v1/auth/refresh` | Refresh token | Rotate the token pair |
| `GET` | `/me` or `/api/v1/auth/me` | Access token | Read the current user identity |
| `GET` | `/api/v1/aws/identity` | Access token | Show the active AWS IAM identity |

Send tokens in the HTTP header:

```http
Authorization: Bearer <access-token>
```

The refresh endpoint expects a refresh token in the same header. Access tokens
are short-lived; refresh tokens are longer-lived and are rotated on refresh.

## AWS Monitoring

`main.py` records request metrics and structured logs. HTTP 5xx responses also
trigger an SNS notification when `SNS_TOPIC_ARN` is configured. AWS credentials
are resolved through the standard boto3 credential chain, so IAM roles are
preferred over long-lived access keys.

## Security Notes

- Set a strong, unique `JWT_SECRET_KEY` in production.
- Use least-privilege IAM policies.
- Do not commit `.env` files, AWS credentials, private keys, or Terraform state.
- Use HTTPS in production.
- Refresh tokens should be stored securely by the client and never exposed in URLs.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
