import os
import boto3
from tonythor.application_support.logger import Logger
from tonythor.application_support.arg_parse import ArgParser as AP


class EnvConfig:
    """a place to set some application wide variables and configurations"""
    path:str = ""
    account_number:str = ""

    def __init__(self) :
        Logger.get_instance(self)
        self.path =  os.path.dirname(os.path.realpath(__file__))
        self.account_number = self.__get_account_number__()

    def __get_account_number__(self) : 
        client = boto3.client("sts")
        return client.get_caller_identity()["Account"]


