import sys
from tonythor.application_support.env_config import EnvConfig
from tonythor.application_support.arg_parse import ArgParser as AP

valid_module_options = ['delete-rule', 'list-rules', 'deploy-rule']

if len(sys.argv) > 1 and sys.argv[1] in valid_module_options:
    args = AP().args
    print(args)
    operation:str = sys.argv[1]
    conf:EnvConfig = EnvConfig()

else : 
    """ use argparse help to tell the user they need at lest one argument"""
    AP()



