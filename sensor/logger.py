import logging
import sys
import os
from datetime import datetime

LOG_FILE =f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#File name will be the time stamp of the file when the log is created.
#datetime.now() will written in numeric format.
#strftime('%m_%d_%Y_%H_%M_%S') is used to format the date and time in the required format.


#Create a folder where these files will be saved
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) #This will create a folder named logs and the log file will be created inside this folder. getcwd() will give the current working directory.
#Now everytime we run the code a new log file will be created in the logs folder.But we have to stop it from creating multiple folders again and again.
os.makedirs(logs_path,exist_ok=True) #This will create the folder/directory if it does not exist. exist_ok=True will not give error if the folder already exists.
LOG_FILE_PATH= os.path.join(logs_path,LOG_FILE) #This will create the complete path of the log file.

logging.basicConfig( #This is used to configure the logging module. basicConfig is a function in logging module.
    filename=LOG_FILE_PATH, 
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", #s is used to convert any variable to string. d is used for integer. %(name) is used to get the name of the logger. %(message) is used to get the logging message. %(asctime) is used to get the time of logging.
    level = logging.INFO,
)