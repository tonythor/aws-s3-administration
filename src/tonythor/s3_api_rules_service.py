import boto3
import logging
from tonythor import conf
import datetime
from datetime import datetime
import sys


class S3ApiRulesService:
    """
    ### The S3 Api Rules Service
    This service handles getting and setting of rules using the s3 api.
    """
    bucket: str
    existing_rules: list
    s3_resource:boto3.Session
 
    def __init__(self, bucket: str):
        self.bucket = bucket
        self.s3_resource = boto3.resource('s3')
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
        blc = self.s3_resource.BucketLifecycleConfiguration(self.bucket)
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
                self.s3_resource.BucketLifecycle(self.bucket).delete()

            if length > 1:
                # Means there is more than one record, so delete just that one matching one from the existing rules
                # and shoot whatever's left back up as a new policy object. 
                del self.existing_rules[delete_position]
                logging.info(f"** Rules AFTER the deletion {self.existing_rules}")
                blc = self.s3_resource.BucketLifecycleConfiguration(self.bucket)
                rules = {'Rules' : self.existing_rules}
                blc.put(LifecycleConfiguration = rules)
        else:
            logging.info("** Nothing to delete, perhaps you types in the wrong rule id?")   
    

    def directories_under_prefix(self, prefix) -> dict:
        ## Returns a recursive dictionary list in the format of {key:str, file_count:int}
        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator('list_objects')
        operation_parameters = {'Bucket': self.bucket,
                                'Prefix': prefix}
        page_iterator = paginator.paginate(**operation_parameters)
        directories = {} 
        separator = "/"

        try:
            for page in page_iterator:
                        # {'Key': 'cloud-trail/AWSLogs/{accountid}/CloudTrail-Digest/af-south-1/2022/10/22/{accountid}_CloudTrail-Digest_af-south-1_tonyfraser-aws-logs_us-east-1_20221022T004127Z.json.gz', 
                        # 'LastModified': datetime.datetime(2022, 10, 22, 1, 24, 16, tzinfo=tzutc()), 
                        # 'ETag': '"6a4408cf509626436b28821199b22ff7"', 
                        # 'Size': 727, 
                        # 'StorageClass': 'STANDARD', 
                        # 'Owner': {'DisplayName': 'tony.fraser', 'ID': 'bb1205f9184eceb6def88d16f60394794f55b07ea847c23a4e41483515d28d5d'}}
                for key_details in page['Contents']:
                    this_key = key_details.get("Key")
                    this_directory = separator.join(this_key.split("/")[0:-1])

                    if directories.get(this_directory):
                        directories[this_directory] = directories[this_directory] + 1
                    else:
                        directories[this_directory] = 1
            return directories
 
        except BaseException:
            logging.error(f"Prefix: {prefix}")
            logging.error("Nothing came back from S3. Are you sure that is a valid prefix?")
            sys.exit(1)