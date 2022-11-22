import boto3
import logging
from tonythor import conf

class S3ApiRulesService:
    """
    ### The S3 Api Rules Service
    This service handles getting and setting of rules using the s3 api.
    """
    bucket: str
    existing_rules: list

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.existing_rules = self.__download__()
    
    def __download__(self) -> list:
        lifecycle_rules_exist = False
        client = boto3.client('s3')
        try:
            client.get_bucket_lifecycle(Bucket=self.bucket).get("Rules")
            lifecycle_rules_exist = True
        except Exception as e:
            if "NoSuchLifecycleConfiguration" in str(e):
                logging.info(f'## Note: There is no lifecycle policy on s3://{self.bucket}.')
            else: 
                logging.info(f"## Exiting because of this exception: {str(e)}.")

        rules = []
        if lifecycle_rules_exist:
            rules: list = client.get_bucket_lifecycle(Bucket=self.bucket).get('Rules')
            logging.info(f"## Found existing rules: {rules}")
        return rules
    

    def upload(self, new_rule: list):
        s3 = boto3.resource('s3')
        blc = s3.BucketLifecycleConfiguration(self.bucket)
        all_rules = {'Rules' : self.existing_rules + new_rule} if self.existing_rules else {'Rules' : new_rule}
        logging.info(f"## Attempting to upload:  {all_rules}")

        try:
            blc.put(LifecycleConfiguration = all_rules)
            logging.info("## Deployed")

        except Exception as e:
            logging.error(f'## Rules were not uploaded. Exception is: {str(e)}')
            ## Possible errors are:
            #  1. Rules were not uploaded. Exception is: An error occurred (InvalidRequest) when calling the 
            #     PutBucketLifecycleConfiguration operation: Found two rules with same 
            #     prefix '/cloud-trail/AWSLogs/764573855117/CloudTrail/'
            #  2. Rules were not uploaded. Exception is: An error occurred (InvalidArgument) when calling 
            #     the PutBucketLifecycleConfiguration operation: Rule ID must be unique. Found 
            #     same ID for more than one rule
            