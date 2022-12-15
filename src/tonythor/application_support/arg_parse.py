import argparse


class ArgParser:
    """ takes in all the arguments, passes them back as a dict, but also
    prepares the rule as a dictionary object in a format that the S3 api 
    can use directly."
    """
    args: dict

    def __init__(self):
        self.args = self.__parse_args__()


    def __parse_args__(self):
        parser = argparse.ArgumentParser(prog="S3RulesAdminUtility")
        subparsers = parser.add_subparsers(help='sub-command help')

        ## Deploy a rule
        parser_deploy_rule = subparsers.add_parser('deploy-rule', help="used to deploy a retention rule to an s3 bucket")
        parser_deploy_rule.add_argument('-e', '--expire_days',
                                    required=True,
                                    dest='expire_days',
                                    help='number of days to expire/delete a an s3 key',
                                    type=int
                                    )
        parser_deploy_rule.add_argument('-k', '--key_prefix',
                                    required=True,
                                    dest="key_prefix",
                                    help='like /cloudtrail/us-east-1/22-01-01/, remember the trailing slash!'
                                    )   
        parser_deploy_rule.add_argument('-b', '--bucket',
                                    required=True,
                                    dest="bucket",
                                    help='s3 bucket name, not s3:// or trailing slash'
                                    )   
        parser_deploy_rule.add_argument('-i', '--rule_id',
                                    required=True,
                                    dest="rule_id",
                                    help='the name of the rule as displayed in the console'
                                    )
        parser_deploy_rule.add_argument('-d', '--disable_dry_run',
                                    action='store_false',
                                    required=False,
                                    help='the default behavior is to run a dry run. disable if you actually want to deploy'
                                    )   
                  

        ## list bucket rules
        parser_list_rules = subparsers.add_parser('list-rules', help="shows retention and transformation rules for a given s3 bucket")
        parser_list_rules.add_argument('-b', '--bucket',
                                    required=True,
                                    dest="bucket",
                                    help='s3 bucket name, not s3:// or trailing slash'
                                    )   

        parser_list_rules.add_argument('-r', '--raw',
                                    action='store_true',
                                    required=False,
                                    help='shows raw output of the rules'
                                    )   

        ## delete a rule
        parser_delete_rule = subparsers.add_parser('delete-rule', help="use this to remove a retention or transition rule from an s3 bucket")
        parser_delete_rule.add_argument('-b', '--bucket',
                                    required=True,
                                    dest="bucket",
                                    help='s3 bucket name, not s3:// or trailing slash'
                                    )  
        parser_delete_rule.add_argument('-i', '--rule_id',
                                    required=True,
                                    dest="rule_id",
                                    help='the name of the rule, as displayed in the console, to delete'
                                    )

        ## expert mode -- upload any isolated json rule                            
        parser_json_rule = subparsers.add_parser('upload-json', help="manage your rules with more complex transitions")
        parser_json_rule.add_argument('-b', '--bucket',
                                    required=True,
                                    dest="bucket",
                                    help='s3 bucket name, not s3:// or trailing slash'
                                    )  
        parser_json_rule.add_argument('-p', '--json_file_path',
                                    required=True,
                                    dest="json_file_path",
                                    help='the file path of the json with the exact rule you want to upload'
                                    )
        parser_json_rule.add_argument('-o', '--overwrite',
                                    action='store_true',
                                    required=False,
                                    help='overwrite the rule if it exists already'
                                    ) 
        parser_json_rule.add_argument('-d', '--disable_dry_run',
                                    action='store_false',
                                    required=False,
                                    help='the default behavior is to run a dry run. disable if you actually want to deploy'
                                    )   
                    
        return parser.parse_args()




