import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


logger = logging.getLogger(__name__)


class CloudWatchIntegration:
	"""Publish application metrics, logs, and notifications to AWS."""

	def __init__(
		self,
		namespace: str = "JwtApi",
		region_name: str | None = None,
		log_group_name: str | None = None,
		sns_topic_arn: str | None = None,
	) -> None:
		# boto3 obtains credentials from an IAM role, profile, or environment.
		region = region_name or os.getenv("AWS_REGION", "us-east-1")
		self.namespace = namespace
		self.log_group_name = log_group_name or os.getenv(
			"CLOUDWATCH_LOG_GROUP", "/jwt-api/application"
		)
		self.log_stream_name = os.getenv("CLOUDWATCH_LOG_STREAM", "flask")
		self.sns_topic_arn = sns_topic_arn or os.getenv("SNS_TOPIC_ARN")
		self.cloudwatch = boto3.client("cloudwatch", region_name=region)
		self.logs = boto3.client("logs", region_name=region)
		self.sns = boto3.client("sns", region_name=region)
		self.sts = boto3.client("sts", region_name=region)
		# CloudWatch Logs uses this token to keep events ordered in a stream.
		self._sequence_token: str | None = None

	def record_metric(self, metric_name: str, value: float = 1, unit: str = "Count") -> None:
		# Publish one application metric in the configured namespace.
		self.cloudwatch.put_metric_data(
			Namespace=self.namespace,
			MetricData=[
				{
					"MetricName": metric_name,
					"Value": value,
					"Unit": unit,
					"Timestamp": datetime.now(timezone.utc),
				}
			],
		)

	def write_log(self, message: str, level: str = "INFO") -> None:
		"""Write one structured application event to CloudWatch Logs."""
		# Create the group and stream lazily so deployment does not need a setup script.
		try:
			self.logs.create_log_group(logGroupName=self.log_group_name)
		except self.logs.exceptions.ResourceAlreadyExistsException:
			pass
		try:
			self.logs.create_log_stream(
				logGroupName=self.log_group_name,
				logStreamName=self.log_stream_name,
			)
		except self.logs.exceptions.ResourceAlreadyExistsException:
			pass

		event = {
			"timestamp": datetime.now(timezone.utc).isoformat(),
			"level": level,
			"message": message,
		}
		request: dict[str, Any] = {
			"logGroupName": self.log_group_name,
			"logStreamName": self.log_stream_name,
			"logEvents": [{"timestamp": int(datetime.now().timestamp() * 1000), "message": json.dumps(event)}],
		}
		if self._sequence_token:
			request["sequenceToken"] = self._sequence_token

		response = self.logs.put_log_events(**request)
		self._sequence_token = response.get("nextSequenceToken")

	def notify(self, subject: str, message: str) -> None:
		# Notifications are optional; monitoring must still work without an SNS topic.
		if not self.sns_topic_arn:
			logger.warning("SNS_TOPIC_ARN is not configured; notification skipped")
			return
		self.sns.publish(TopicArn=self.sns_topic_arn, Subject=subject[:100], Message=message)

	def caller_identity(self) -> dict[str, str]:
		"""Return the IAM identity selected by the boto3 credential chain."""
		# STS confirms which IAM role or user is actually being used.
		response = self.sts.get_caller_identity()
		return {
			"account": response["Account"],
			"arn": response["Arn"],
			"user_id": response["UserId"],
		}

	def safely_record(self, metric_name: str, value: float = 1) -> None:
		try:
			self.record_metric(metric_name, value)
		except (BotoCoreError, ClientError) as error:
			logger.warning("CloudWatch metric failed: %s", error)

	def safely_write_log(self, message: str, level: str = "INFO") -> None:
		try:
			self.write_log(message, level)
		except (BotoCoreError, ClientError) as error:
			logger.warning("CloudWatch log failed: %s", error)

	def safely_notify(self, subject: str, message: str) -> None:
		try:
			self.notify(subject, message)
		except (BotoCoreError, ClientError) as error:
			logger.warning("SNS notification failed: %s", error)


