from singleton import SingletonLogger
from threading import Thread

def main2():
    singleton_logger_1 = SingletonLogger.get_instance()
    singleton_logger_2 = SingletonLogger.get_instance()

    if singleton_logger_1 == singleton_logger_2:
        print("Same instance, singletone pattern correctly implemented")

def test_threadsafe_singleton(thread_id):
    logger = SingletonLogger.get_instance()
    print("Instance type: ", type(logger))
    logger.log(f"Logger instance from Thread-{thread_id}: {id(logger)}")


def main2():
    t1 = Thread(target=test_threadsafe_singleton, args=(1,))
    t2 = Thread(target=test_threadsafe_singleton, args=(2,))

    t1.start()
    t2.start()


    t1.join()
    t2.join()

    # Check in main thread as well
    logger1 = SingletonLogger.get_instance()
    logger2 = SingletonLogger.get_instance()

    if logger1 == logger2:
        print("Same instance, singleton pattern correctly implemented.")
    else:
        print("Different instances, something is wrong.")

if __name__ == "__main__":
    # first example
    # main1()
    

    # second example
    main2()
