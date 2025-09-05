import sys 
import os


def error_message_detail(error, error_detail:sys):#This fn will capture more details about the errors like what error, in which file and which ine.
    _,_,exc_tb = error_detail.exc_info() #This exc_info() is a function in sys library which will help us give info about error.
    #exc_info() will return three things in a tuple where first and second are useless but third is usefull which is stored in exc_tb.
    filename = exc_tb.tb_frame.f_code.co_filename #to get the filename where the error has occured.

    error_message="Error occured and the file name is [{0}] and the line no is [{1}] and the error is[{2}]".format(
        filename,exc_tb.tb_lineno,str(error))
    
    return error_message



class SensorException(Exception): #Exception is a superclass that we have inherited.
    def __init__(self, error_message, error_detail:sys): #self to say it is constructor, error_message is a variable, error_detail is another variable which will be using sys library
        super().__init__(error_message) #super() fn is used to use the inherited function in python here we will use Exception class.

        self.error_message = error_message_detail(error_message, error_detail=error_detail) #calling the function to get the error message details.

    def __str__(self): #string representation of the object
        return self.error_message