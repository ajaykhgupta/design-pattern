from threading import Lock
from enum import Enum



class LogLevel(Enum):
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    ERROR = 'ERROR'


class Logger:
    _instance = None
    _lock: Lock = Lock()

    def __init__(self):
        raise RuntimeError("This is a singleton, invoke get_instance() ")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls.__new__(cls)

                    # open a logging file
                    cls._instance._log_file = open("logger.log", "a")
        return cls._instance


    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        formatted_message = f"[{level.value}] {message} "
        print(formatted_message)
        self._log_file.write(formatted_message + "\n")

    
    def __del__(self):

        if hasattr(self, '_log_file'):
            self._log_file.close()

if __name__ == "__main__":
    logger = Logger.get_instance()
    logger.log("This is an info message.")
    logger.log("This is a debug message.", LogLevel.DEBUG)
    logger.log("Something went wrong!", LogLevel.ERROR)
    logger.log("This is an info message.")
    logger.log("This is an info message.")




