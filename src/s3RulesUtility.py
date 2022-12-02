from tonythor import conf, args, operation
from tonythor.s3_api_rules_service import S3ApiRulesService 
import logging

service = S3ApiRulesService(bucket = args.bucket)
logging.info(f"*** Using account number: {conf.account_number}")

# todo - check permissions here, before uploading or deleting

match operation :
    case "list-rules":
        # python -m s3RulesUtility list-rules --bucket tonyfraser-aws-logging
        # python -m s3RulesUtility list-rules --bucket tonyfraser-aws-logging --raw
        if service.existing_rules:
            for rule in service.existing_rules:
                if args.raw:
                    logging.info(f'*** Rule: {rule}')
                else:
                    logging.info(f'*** RuleID: {rule.get("ID")}')
        else:
            logging.info("'*** No rules for this bucket")        
                    
    case "deploy-rule": 
        # python -m s3RulesUtility deploy-rule -e 45 -k cloud-trail/AWSLogs/  -b tonyfraser-aws-logging -i delete-cloud-trail-over-45
        # python -m s3RulesUtility deploy-rule -e 23 -k mykey/is/a/good/key23 -b tonyfraser-aws-logging -i 23-days-is-a-good-key
        # python -m s3RulesUtility deploy-rule -e 27 -k mykey/is/a/good/key27 -b tonyfraser-aws-logging -i 27-days-is-a-good-key
        inbound_rule = [{
            'Expiration': { 'Days': args.expire_days},
            'ID': args.rule_id,
            'Prefix': args.key_prefix,
            'Status': 'Enabled',
            }] 
        service.upload(inbound_rule)

    case 'delete-rule': 
        # python -m s3RulesUtility delete-rule --bucket tonyfraser-aws-logging --rule_id 23-days-is-a-good-key
        # python -m s3RulesUtility delete-rule --bucket tonyfraser-aws-logging --rule_id delete-cloud-trail-over-45
        service.delete_rule(args.rule_id)

