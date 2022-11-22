# aws-s3-administration
A repo with a bunch of shell scripts for managing S3 retention and transformation rules. It might also have some CDK or SAM scripts, we'll see where this goes. 

I use it for managing my personal aws account.

### To install/activate this project
```
# 1. Make sure you have your ~/.aws/credentials files set up

# 2. git clone this project, cd into the project directory
python3 -m venv .venv     # build your project virtual env 
source .venv/bin/activate # activate your virual env
.venv/bin/python -m pip install -r ./requirements.txt
```

### some useful commands

``` 
cd ./src/
python -m tonythor.examples.deploy_rule # go edit it to your liking first. 
python -m main


```
