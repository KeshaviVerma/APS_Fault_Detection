from sensor.exception import SensorException
import sys
import os       

from sensor.logger import logging

def test_exception():
    try:
        logging.info("Testing exception handling for division by zero")
        a = 1/0
    except Exception as e:
        raise SensorException(e, sys) #raising the exception again so that it can be handled by the caller function.

if __name__ == "__main__": #module will be executed only when we run this file directly not when we import this file. And only this file will be executed not the other files.  
    try:
        test_exception()
    except Exception as e:
        print(e) 