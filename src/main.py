from tonythor import conf
from tonythor.rules import Rules

print(conf.account_number)
rules = Rules(bucket = "tonyfraser-aws-logging")
print(rules.existing_rules)
