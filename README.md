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

### usage
``` 
source .venv/bin/activate
cd ./src/
# python -m tonythor.examples.deploy_rule  -> if you want to use as a script. 
python -m main -e 45 -i delete-cloud-trail-over-45 -k cloud-trail/AWSLogs/ -b tonyfraser-aws-logging
```
