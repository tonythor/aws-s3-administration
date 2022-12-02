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
    s3:boto3.Session


    def __init__(self, bucket: str):
        self.bucket = bucket
        self.s3 = boto3.resource('s3')
        self.existing_rules = self.__download__()
    
    def __download__(self) -> list:
        lifecycle_rules_exist = False
        client = boto3.client('s3')
        try:
            client.get_bucket_lifecycle(Bucket=self.bucket).get("Rules")
            lifecycle_rules_exist = True
        except Exception as e:
            if "NoSuchLifecycleConfiguration" in str(e):
                logging.info(f'**! There is no lifecycle policy on s3://{self.bucket}.')
            else: 
                logging.info(f"**! Exiting because of this exception: {str(e)}.")

        rules = []
        if lifecycle_rules_exist:
            rules: list = client.get_bucket_lifecycle(Bucket=self.bucket).get('Rules')
        return rules
    

    def upload(self, new_rule: list):
        blc = self.s3.BucketLifecycleConfiguration(self.bucket)
        all_rules = {'Rules' : self.existing_rules + new_rule} if self.existing_rules else {'Rules' : new_rule}
        logging.info(f"** Attempting to upload:  {all_rules}")

        try:
            blc.put(LifecycleConfiguration = all_rules)
            logging.info("** Deployed")

        except Exception as e:
            logging.error(f'** Rules were not uploaded. Exception is: {str(e)}')
            ## Possible errors are:
            #  1. Rules were not uploaded. Exception is: An error occurred (InvalidRequest) when calling the 
            #     PutBucketLifecycleConfiguration operation: Found two rules with same 
            #     prefix '/cloud-trail/AWSLogs/764573855117/CloudTrail/'
            #  2. Rules were not uploaded. Exception is: An error occurred (InvalidArgument) when calling 
            #     the PutBucketLifecycleConfiguration operation: Rule ID must be unique. Found 
            #     same ID for more than one rule

    def delete_rule(self, rule_id):
        # takes in one rule name, deletes it from the list, runs delete all rules, then re-uploads the rules
        # todo: make sure the user has the s3:PutLifecycleConfiguration permission
        i = 0
        length = len(self.existing_rules)
        delete_position = None

        while i < length:
            if self.existing_rules[i].get("ID") == rule_id:
                delete_position = i 
            i += 1
         
        
        # if delete position is not null, it means that there's something in existing rules
        # where the title matched, and it needs to be deleted.
        if delete_position != None:
            if length == 1:
                # This means there only one rule, so you have to deregister the lifecycle policy itself.
                # You can't upload an "empty" set of rules.
                logging.info('** deregistering bucket lifecycle policy')   
                self.s3.BucketLifecycle(self.bucket).delete()

            if length > 1:
                # Means there is more than one record, so delete just that one matching one from the existing rules
                # and shoot whatever's left back up as a new policy object. 
                del self.existing_rules[delete_position]
                logging.info(f"** Rules AFTER the deletion {self.existing_rules}")
                blc = self.s3.BucketLifecycleConfiguration(self.bucket)
                rules = {'Rules' : self.existing_rules}
                blc.put(LifecycleConfiguration = rules)
        else:
            logging.info("** Nothing to delete, perhaps you types in the wrong rule id?")   

