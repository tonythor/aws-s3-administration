import boto3
import pprint

# You should probably set your PYTHONPATH to whatever your airflow triggers conda/venv is.  

# Edit and set your variables first
rule_id_string='deleteCloudTrailAfter30DaysWTrailingSlash200'
bucket = 'tonyfraser-aws-logging'
key_prefix=f'cloud-trail/AWSLogs/'
expire_time_in_days=200

# s3://tonyfraser-aws-logging/cloud-trail/AWSLogs/764573855117/CloudTrail/us-east-1/2022/08/19/

# don't change anything below this
lifecycle_rules_exist = False
new_rule={ 
    'Expiration': { 'Days': expire_time_in_days},
    'ID': rule_id_string,
    'Prefix': key_prefix,
    'Status': 'Enabled',
}


## Sanity check, first look and see if there's lifecycle policy at all.
client = boto3.client('s3')
try:
    client.get_bucket_lifecycle(Bucket=bucket).get("Rules")
    lifecycle_rules_exist = True
except Exception as e:
    if "NoSuchLifecycleConfiguration" in str(e):
        print(f'## Note: There is no lifecycle policy on s3://{bucket}. We will now deploy the first.')
    else: 
        print(f"Exiting because of this exception: {str(e)}.")
        quit()


# If rules exist, get them, else, use the one above only
rules = []
if lifecycle_rules_exist:
    rules: list = client.get_bucket_lifecycle(Bucket=bucket).get('Rules')
    print(f"## Found these existing rules:")
    pprint.pp(rules)
    rules.append(new_rule)
else: 
    rules = [new_rule]


# Prepare the lifecycle call
s3 = boto3.resource('s3')
blc = s3.BucketLifecycleConfiguration(bucket)
print("## Deploying the following rules:")
rules_to_deploy = {"Rules" : rules}
pprint.pp(rules_to_deploy)

# send it, or fail and tell why.
try:
    blc.put(LifecycleConfiguration = rules_to_deploy)
    print("Deployed")

except Exception as e:
    print(f'## Rules were not uploaded. Exception is: {str(e)}')
    ## Possible errors are:
    #  1. Rules were not uploaded. Exception is: An error occurred (InvalidRequest) when calling the 
    #     PutBucketLifecycleConfiguration operation: Found two rules with same 
    #     prefix '/cloud-trail/AWSLogs/764573855117/CloudTrail/'
    #  2. Rules were not uploaded. Exception is: An error occurred (InvalidArgument) when calling 
    #     the PutBucketLifecycleConfiguration operation: Rule ID must be unique. Found 
    #     same ID for more than one rule
