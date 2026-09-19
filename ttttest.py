import boto3 
import logging
from datetime import timezone, timedelta, datetime


logger = logging.getLogger(__name__)



class CloudWatch: 
    def __init__(self, cloudwatch_source_name, region_name='us-east-1'):
        self.cloudwatch_resource = boto3.resource('cloudwatch', region_name=region_name)
        self.cloudwatch_client = boto3.client('cloudwatch', region_name=region_name)
        self.cloudwatch_source_name = cloudwatch_source_name

        

    def put_metric_data(self , metric_name , value , unit , name):
        try:
            response = self.cloudwatch_client.put_metric_data(
                Namespace=self.cloudwatch_source_name,
                MetricData=[
                    {
                        'failure_count': 0,
                        'Timestamp': datetime.now(timezone.utc),
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': unit,
                        'Dimensions': [
                            {
                                'Name': 'Name',
                                'Value': name
                            }
                        ]
                    }
                ]
            )
            logger.info("Metric data put successfully")
        except Exception as e:
            logger.error(f"Error occurred while putting metric data: {e}")

    def set_metric_data(self , metric_name , value , unit , name , data_set , timestamp):
        try:
            response = self.cloudwatch_client.put_metric_data(
                Namespace=self.cloudwatch_source_name,
                MetricData=[
                    {
                        'failure_count': 0,
                        'Timestamp': datetime.now(timezone.utc),
                        'MetricName': metric_name,
                        'Value': [data_set["value"]],
                        'Unit': unit,
                        'counts' : data_set["counts"],
                        'Dimensions': [
                            {
                                'Name': 'Name',
                                'Value': name
                            }
                        ]
                    }
                ]
            )
            logger.info("Metric data set successfully: %s", name , metric_name , value , unit , data_set , timestamp)
        except Exception as e:
            logger.error(f"Error occurred while setting metric data: {e}")


    def list_metrics(self):
        try:
            kwargs = {
                'Namespace': self.cloudwatch_source_name
            }
            response = self.cloudwatch_client.list_metrics(
                Namespace=self.cloudwatch_source_name
            )
            logger.info("Metrics listed successfully")
            return response['Metrics']
        except Exception as e:
            logger.error(f"Error occurred while listing metrics: {e}")
            return None

    def get_metric_statistics(self, metric_name, start_time, end_time, period, statistics):
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace=self.cloudwatch_source_name,
                MetricName=metric_name,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=statistics
            )
            logger.info("Metric statistics retrieved successfully")
            return response['Datapoints']
        except Exception as e:
            logger.error(f"Error occurred while getting metric statistics: {e}")
            return None

    def create_alarm(self, alarm_name, metric_name, threshold, comparison_operator, evaluation_periods, period, statistic):
        try:
            response = self.cloudwatch_client.put_metric_alarm(
                AlarmName=alarm_name,
                MetricName=metric_name,
                Namespace=self.cloudwatch_source_name,
                Threshold=threshold,
                ComparisonOperator=comparison_operator,
                EvaluationPeriods=evaluation_periods,
                Period=period,
                Statistic=statistic
            )
            logger.info("Alarm created successfully")
        except Exception as e:
            logger.exception(
                f"Error occurred while creating alarm: {e} | "
                f"AlarmName: {alarm_name}, MetricName: {metric_name}, "
                f"Threshold: {threshold}, ComparisonOperator: {comparison_operator}, "
                f"EvaluationPeriods: {evaluation_periods}, Period: {period}, Statistic: {statistic}"
            )
            raise
        else:
            return alarm_name

    def get_metric_alarms(self, alarm_name: str , metric_name: str , metric_namespace: str )-> dict:
        failed_attempts = 0
        metric = self.cloudwatch_resource.Metric(metric_namespace, metric_name)
        alarm_tier = metric.alarms.all()
        
        for alarm in alarm_tier:
            try:
                logger.info(f"Alarm Name: {alarm.name}, State: {alarm.state_value}, "
                            f"Threshold: {alarm.threshold}, Comparison Operator: {alarm.comparison_operator}, "
                            f"Evaluation Periods: {alarm.evaluation_periods}, Period: {alarm.period}, "
                            f"Statistic: {alarm.statistic}")
                logger.info(f"Alarm Actions: {alarm.alarm_actions}, OK Actions: {alarm.ok_actions}, "
                            f"Insufficient Data Actions: {alarm.insufficient_data_actions}, "
                            f"State Reason: {alarm.state_reason}, State Updated Timestamp: {alarm.state_updated_timestamp}, "
                            f"failure_count: {alarm.failure_count}, Datapoints to Alarm: {alarm.datapoints_to_alarm}")
            except Exception as alarm_error:
                failed_attempts += 1
                logger.error(f"Error processing alarm: {alarm_error}")
        
        try:
            if alarm_name:
                response = self.cloudwatch_client.describe_alarms(
                    AlarmNames=[alarm_name]
                )
            else:
                response = self.cloudwatch_client.describe_alarms()
            logger.info(f"Metric alarms retrieved successfully with {failed_attempts} failed attempts")
            return {
                'alarms': response['MetricAlarms'],
                'failed_attempts': failed_attempts
            }
        except Exception as e:
            failed_attempts += 1
            logger.error(f"Error occurred while getting metric alarms: {e}. Total failed attempts: {failed_attempts}")
            return {
                'alarms': None,
                'failed_attempts': failed_attempts
            }

    def configure_alarm_actions(self, alarm_name: str, alarm_actions: list, ok_actions: list, insufficient_data_actions: list):
        try:
            response = self.cloudwatch_client.put_metric_alarm(
                AlarmName=alarm_name,
                AlarmActions=alarm_actions,
                OKActions=ok_actions,
                InsufficientDataActions=insufficient_data_actions
            )
            logger.info(f"Alarm actions configured successfully for alarm: {alarm_name}")
            return response
        except Exception as e:
            logger.error(f"Error occurred while configuring alarm actions for alarm {alarm_name}: {e}")
            return None
