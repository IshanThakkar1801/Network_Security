import sys

class NetworkSecurityException(Exception):

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)

        self.error_message = error_message

        _, _, exc_tb = error_detail.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in python script [{self.file_name}] line number [{self.lineno}] error message [{self.error_message}]"