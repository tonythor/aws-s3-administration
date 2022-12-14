# aws-s3-administration
A repo that uploads s3 retention policies to buckets. Has good clean failure logic.  
I use it for managing my personal aws account.

### To install/activate this project

1. Make sure you have your ~/.aws/credentials files in place.
1. git clone this project, cd into the project directory
1. build the virtual env 
```shell
python3 -m venv .venv     # build your project virtual env 
source .venv/bin/activate # activate your virual env
.venv/bin/python -m pip install --upgrade pip 
.venv/bin/python -m pip install -r ./requirements.txt
```

### Usage / Upload an s3 retention rule 
Notes: 
1. `python -m tonythor.examples.deploy_rule` is the original POC
1. If your key is a directory, include the trailing slash or your rule won't work
1. All deploy-rule calls are are validated with a dry run by default. You have to add a flag to disable this behavior. That flag appears at the end of the validation step.

``` 
source .venv/bin/activate

cd ./src/

python -m s3RulesUtility list-rules --bucket {bucket}
python -m s3RulesUtility list-rules --bucket {bucket} --raw

python -m s3RulesUtility deploy-rule -e 45 -k cloud-trail/AWSLogs/  -b {bucket} -i delete-cloud-trail-over-45
python -m s3RulesUtility deploy-rule -e 23 -k mykey/is/a/good/key23 -b {bucket} -i 23-days-is-a-good-key

python -m s3RulesUtility delete-rule --bucket {bucket} --rule_id delete-cloud-trail-over-45
python -m s3RulesUtility delete-rule --bucket {bucket} --rule_id 23-days-is-a-good-key

python -m s3RulesUtility upload-json --bucket {bucket} -p ../sample_conf/rule.json
```

Note: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_lifecycle_configuration
