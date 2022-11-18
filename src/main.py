import logging

from tonythor import conf
from tonythor.rules_service import RulesService

logging.info(f"Using account number: {conf.account_number}")
rules_service = RulesService(bucket = "tonyfraser-aws-logging")
