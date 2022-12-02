import logging
import logging.handlers

class Logger:
    """
    ## Overview
    - A singleton to control/centralize logging, make sure it all goes to one place.
    - See envconfig's __init__() method. 
    """
    __instance = None

    @staticmethod
    def get_instance(self):
        if Logger.__instance is None:
            Logger().__init__()
        return Logger.__instance

    def __init__(self, log_file_name='./run.log'):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            log_format_str = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
            logging.basicConfig(format=log_format_str,
                                datefmt='%Y %m %d - %H:%M:%S',
                                level=logging.INFO,
                                handlers=[
                                    logging.FileHandler(log_file_name),
                                    logging.StreamHandler()
                                ])
            logging.captureWarnings(True)

        self.__instance = self

       