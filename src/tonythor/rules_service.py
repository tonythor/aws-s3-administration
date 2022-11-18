import boto3
import logging
from tonythor import conf

class RulesService:
    """
    ## The Rules Service
    This service gets and sends rules via the s3Api  

    """
    bucket: str
    existing_rules: list

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.existing_rules = self.__get_from_server__()
    
    def __get_from_server__(self) -> list:
        client = boto3.client('s3')
        try:
            client.get_bucket_lifecycle(Bucket=self.bucket).get("Rules")
            lifecycle_rules_exist = True
        except Exception as e:
            if "NoSuchLifecycleConfiguration" in str(e):
                logging.info(f'## Note: There is no lifecycle policy on s3://{bucket}.')
            else: 
                logging.info(f"Exiting because of this exception: {str(e)}.")

        rules = []
        if lifecycle_rules_exist:
            rules: list = client.get_bucket_lifecycle(Bucket=self.bucket).get('Rules')
            logging.info(f"## Found these existing rules: {rules}")
        return rules

        




