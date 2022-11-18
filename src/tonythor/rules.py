import boto3
import pprint 

class Rules:
    bucket: str
    existing_rules: list

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.existing_rules = self.get()


    def get(self) -> list:
        client = boto3.client('s3')
        try:
            client.get_bucket_lifecycle(Bucket=self.bucket).get("Rules")
            print("here")
            lifecycle_rules_exist = True
        except Exception as e:
            if "NoSuchLifecycleConfiguration" in str(e):
                print(f'## Note: There is no lifecycle policy on s3://{bucket}.')
            else: 
                print(f"Exiting because of this exception: {str(e)}.")

        rules = []
        if lifecycle_rules_exist:
            rules: list = client.get_bucket_lifecycle(Bucket=self.bucket).get('Rules')
            print(f"## Found these existing rules:")
            print(rules)

        self.existing_rules = rules





