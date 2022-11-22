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
                logging.info(f'## Note: There is no lifecycle policy on s3://{bucket}.')
            else: 
                logging.info(f"Exiting because of this exception: {str(e)}.")

        rules = []
        if lifecycle_rules_exist:
            rules: list = client.get_bucket_lifecycle(Bucket=self.bucket).get('Rules')
            logging.info(f"## Found these existing rules: {rules}")
        return rules
    
    # def __merge__(self, new_rule: list) -> dict: 
    #     all__rules = new_rule + 
    #     return_val =  {'Rules':  all__rules}
    #     logging.info(return_val)
        
    #     return return_val
        # {'Rules': [{'Expiration': {'Days': 30},
        #             'ID': 'deleteCloudTrailAfter30DaysWTrailingSlash',
        #             'Prefix': 'cloud-trail/AWSLogs/764573855117/CloudTrail/us-east-1/',
        #             'Status': 'Enabled'},
        #            {'Expiration': {'Days': 200},
        #             'ID': 'deleteCloudTrailAfter30DaysWTrailingSlash200',
        #             'Prefix': 'cloud-trail/AWSLogs/764573855117/CloudTrail/us-east-1/',
        #             'Status': 'Enabled'}]}



    def upload(self, new_rule: list):
        s3 = boto3.resource('s3')
        blc = s3.BucketLifecycleConfiguration(self.bucket)
        
        logging.info("*** Deploying these rules ***")
        logging.info(f"New rule ** {new_rule} ** ")
        logging.info(f"Inbound rule ** {conf.inbound_rule} **")


        all_rules = {'Rules' : self.existing_rules + new_rule}

        logging.info(all_rules)

        # send it, or fail and tell why.
        try:
            blc.put(LifecycleConfiguration = all_rules)
            logging.info("Deployed")

        except Exception as e:
            logging.error(f'## Rules were not uploaded. Exception is: {str(e)}')
            ## Possible errors are:
            #  1. Rules were not uploaded. Exception is: An error occurred (InvalidRequest) when calling the 
            #     PutBucketLifecycleConfiguration operation: Found two rules with same 
            #     prefix '/cloud-trail/AWSLogs/764573855117/CloudTrail/'
            #  2. Rules were not uploaded. Exception is: An error occurred (InvalidArgument) when calling 
            #     the PutBucketLifecycleConfiguration operation: Rule ID must be unique. Found 
            #     same ID for more than one rule

        




