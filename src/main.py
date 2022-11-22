import logging
from tonythor import conf
from tonythor.s3_api_rules_service import S3ApiRulesService


logging.info(f"Using account number: {conf.account_number}")
service = S3ApiRulesService(bucket = conf.bucket)
service.upload(conf.inbound_rule)

