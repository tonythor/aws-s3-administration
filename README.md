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
.venv/bin/python -m pip install -r ./requirements.txt
```

### Usage / Upload an s3 retention rule 
Notes: 
1. `python -m tonythor.examples.deploy_rule` is the original POC
1. If your key is a directory, don't forget to include the trailing slash.
``` 
source .venv/bin/activate
cd ./src/
python -m main -e 45 -i delete-cloud-trail-over-45 -k cloud-trail/AWSLogs/ -b {bucket}
python -m main --expire_days 1000 --rule_id delete-cloud-trail-over-4asdfs5 --key_prefix cloud-trailafasf/AWSLogs/ --bucket {bucket}

```
