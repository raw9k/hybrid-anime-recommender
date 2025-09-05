import sys
    
class CustomException(Exception):
    def __init__(self, error_message, error_details):
        self.error_message = error_message
        # error_details should be a tuple (exc_type, exc_value, exc_tb)
        exc_tb = None
        if error_details and len(error_details) == 3:
            exc_tb = error_details[2]
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = "N/A"
            self.file_name = "N/A"

    def __str__(self):
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )