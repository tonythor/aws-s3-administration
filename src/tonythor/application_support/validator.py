from tonythor.application_support.logger import Logger
import logging
from tonythor import conf, args, operation
from tonythor.s3_api_rules_service import S3ApiRulesService 

class Validator:
    """ instantiated during dry run only """
    subdirectory_count:int
    service:S3ApiRulesService
    impact_check:bool
    prefix_check:bool
    close:bool
    prefix:str

    def __init__(self, service, prefix, impact_check=True, prefix_check=True, close=True, subdirectory_count=4):
        Logger.get_instance(self)
        self.impact_check = impact_check
        self.prefix_check = prefix_check
        self.close = close
        self.service = service
        self.subdirectory_count = subdirectory_count
        self.prefix = prefix

    def validate(self):
        logging.info("* Running deploy rule validator")
        if self.impact_check: self.show_impact()
        if self.prefix_check: self.check_prefix_common_sense()
        if self.close: self.show_closing_messages()

    def show_impact(self):
        logging.info("** Impact Check:")
        logging.info(f"** Dry run with against prefix: {self.prefix}")
        all_keys = self.service.directories_under_prefix(self.prefix)
        logging.info(f'***|> Prefix {self.prefix}')
        for k in all_keys:    
            logging.info(f"***|--> SubDir: {k.replace(self.prefix, './')}  FileCount:{all_keys.get(k)}")
        logging.info(f"*** Your rule will apply to {len(all_keys)} subdirectories and {sum(all_keys.values())} files")   
          
    def check_prefix_common_sense(self):
        _prefix_count_ = self.prefix.count("/")
        logging.info("** Prefix Check:")
        if _prefix_count_ <= 1 :
            logging.info("**** You are likely adding an aggressive rule, similar to rm -fr. ")
            logging.info("**** Please look closely at your key_prefix, and remember that anything under that will be deleted or transitioned.")
        elif self.subdirectory_count > _prefix_count_: 
            logging.info(f"**** Your key only has {_prefix_count_} subdirectories.")
            logging.info(f"**** Please attempt to a little further and reduce the footprint of this rule")  
            logging.info(f"**** And please remember, anything under that will be deleted or transitioned.")          
        else:
            logging.info(f"*** Your key has {_prefix_count_} subdirectories.")
            logging.info(f"This seems reasonable, but please double check and see if you further reduce scope.")
            logging.info(f"**** And please remember, anything under that will be deleted or transitioned.")  
                    
    def show_closing_messages(self):    
        logging.info(f"* Validation Complete")
        logging.info(f"* Add the --disable_dry_run flag to deploy") 
