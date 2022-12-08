from tonythor import conf, args, operation
from tonythor.s3_api_rules_service import S3ApiRulesService 
from tonythor.application_support.validator import Validator
import logging
import pprint


service = S3ApiRulesService(bucket = args.bucket)
logging.info(f"*** Using account number: {conf.account_number}")
logging.info(f"*** System fully initialized")

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
            # *** There are no rules for this bucket, but this is logged within the service. 
            pass
             
                    
    case "deploy-rule": 
        if args.disable_dry_run:
            v = Validator(service = service)
            v.validate()
        else: 
            # python -m s3RulesUtility deploy-rule -e 45 -k cloud-trail/AWSLogs/   -i delete-ctrail-over-45 --dry_run_disabled -b {bucket}
            # python -m s3RulesUtility deploy-rule -e 23 -k mykey/is/a/good/key23  -i 23-days-is-a-good-key --dry_run_disabled -b {bucket}}
            # python -m s3RulesUtility deploy-rule -e 27 -k mykey/is/a/good/key27  -i 27-days-is-a-good-key --dry_run_disabled -b {bucket} 
            inbound_rule = [{
                'Expiration': { 'Days': args.expire_days},
                'ID': args.rule_id,
                'Prefix': args.key_prefix,
                'Status': 'Enabled',
                }] 
            service.upload(inbound_rule)

    case 'delete-rule': 
        # python -m s3RulesUtility delete-rule --bucket tonyfraser-aws-logging --rule_id 23-days-is-a-good-key
        # python -m s3RulesUtility delete-rule --bucket tonyfraser-aws-logging --rule_id delete-ctrail-over-45 
        service.delete_rule(args.rule_id)
