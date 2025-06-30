

# # BASIC Singleton example.
# class SingletonLogger:

#     _instance = None

#     def __init__(self):
#         raise RuntimeError("This is a Singleton, invoke get_instance() instead.")

#     @classmethod
#     def get_instance(cls):
#         if cls._instance is None:
#             cls._instance = cls.__new__(cls)
#         return cls._instance
    
#     def log(self, ex: Exception):
#         print(ex)
    
#     def log(self, message: str):
#         print(message)


# Advance example which also takes care of multithreading (i.e thread safe).
from threading import Lock


class SingletonLogger:

    _instance = None
    _lock = Lock()

    def __init__(self):
        raise RuntimeError("This is a Singleton, invoke get_instance() instead.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls.__new__(cls)
        return cls._instance
    
    def log(self, ex: Exception):
        print(ex)
    
    def log(self, message: str):
        print(message)
