import os
import boto3

class EnvConfig:
    path:str = ""
    account_number:str = ""

    def __init__(self) :
        self.path =  os.path.dirname(os.path.realpath(__file__))
        self.account_number = self.__get_account_number__()

    def __get_account_number__(self) : 
        client = boto3.client("sts")
        return client.get_caller_identity()["Account"]
       