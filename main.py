import os

# 1. Import components from the project modules
from cloudwatch import CloudWatchIntegration
from jwt_config import create_app

# 2. Initialize AWS integrations
# Configuration is loaded automatically from environment variables.
cw = CloudWatchIntegration(
    namespace=os.environ.get("CLOUDWATCH_NAMESPACE", "JwtApi"),
    log_group_name=os.environ.get("CLOUDWATCH_LOG_GROUP", "/jwt-api/application"),
)

# 3. Initialize the application with optional AWS monitoring.
app = create_app(monitoring=cw)

if __name__ == "__main__":
    # Start the application.
    # Ensure JWT_SECRET_KEY and AWS credentials are configured in the environment.
    app.run(host="0.0.0.0", port=5000, debug=False)