from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os,sys


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                        data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            
            self.data_validation_config=data_validation_config
            
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH) #reading the schema file to get the required number of columns and numerical columns because we will use this information to validate the data. We are reading the schema file in the constructor because we will use this information in multiple methods of this class. So we are reading it once and storing it in a variable and then using that variable in the methods. If we read the schema file in each method then it will be a redundant code and also it will be a performance issue because we will be reading the same file multiple times. So we are reading it once and storing it in a variable and then using that variable in the methods.
        
        except Exception as e:
            raise  SensorException(e,sys)
    

    def drop_zero_std_columns(self,dataframe):  #drop columns which have zero standard deviation because those columns will not contribute to the model performance and also it will create problem for model training because of zero variance. So we are dropping those columns.
        pass


    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:     #validating the number of columns in the dataframe with the number of columns in the schema file because if the number of columns in the dataframe is less than the number of columns in the schema file then it means that some columns are missing in the dataframe and those missing columns will create problem for model training because those columns will be used for model training. So we are validating the number of columns in the dataframe with the number of columns in the schema file and if the number of columns in the dataframe is less than the number of columns in the schema file then we are returning False otherwise we are returning True.
        try:
            number_of_columns = len(self._schema_config["columns"])    #getting the number of columns from the schema file because we will use this information to validate the number of columns in the dataframe. We are getting this information from the schema file because we can change the number of columns in the schema file without changing the code and also it will be a good practice to keep this information in the schema file because it will be easy to maintain and also it will be easy to understand for other developers who will work on this code in future. So we are getting this information from the schema file and then we are validating the number of columns in the dataframe with this information and if the number of columns in the dataframe is less than this information then we are returning False otherwise we are returning True.
            
            logging.info(f"Required number of columns: {number_of_columns}")    #logging the required number of columns from the schema file because it will be helpful for debugging and also it will be helpful for understanding the code for other developers who will work on this code in future. So we are logging the required number of columns from the schema file and then we are validating the number of columns in the dataframe with this information and if the number of columns in the dataframe is less than this information then we are returning False otherwise we are returning True.
            
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")    #logging the number of columns in the dataframe because it will be helpful for debugging and also it will be helpful for understanding the code for other developers who will work on this code in future. So we are logging the number of columns in the dataframe and then we are validating the number of columns in the dataframe with the required number of columns from the schema file and if the number of columns in the dataframe is less than the required number of columns from the schema file then we are returning False otherwise we are returning True.
            
            if len(dataframe.columns)==number_of_columns:               #validating the number of columns in the dataframe with the required number of columns from the schema file and if the number of columns in the dataframe is less than the required number of columns from the schema file then we are returning False otherwise we are returning True.
                return True
            return False
        
        except Exception as e:
            raise SensorException(e,sys)


    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:    #validating the numerical columns in the dataframe with the numerical columns in the schema file because if the numerical columns in the dataframe are less than the numerical columns in the schema file then it means that some numerical columns are missing in the dataframe and those missing numerical columns will create problem for model training because those numerical columns will be used for model training. So we are validating the numerical columns in the dataframe with the numerical columns in the schema file and if the numerical columns in the dataframe are less than the numerical columns in the schema file then we are returning False otherwise we are returning True.
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True         
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present=False
                    missing_numerical_columns.append(num_column)
            
            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return numerical_column_present
        
        except Exception as e:
            raise SensorException(e,sys)


    @staticmethod                                              #static method because we will use this method in the detect_dataset_drift method and we will pass the base dataframe and current dataframe to this method and it will return the drift status. So we are making this method static because we don't need to access any instance variable in this method and also it will be a good practice to make this method static because it will be easy to understand for other developers who will work on this code in future. So we are making this method static and then we are using this method in the detect_dataset_drift method to detect the data drift between the base dataframe and current dataframe.
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)                         #reading the data from the file path because we will use this data to validate the data and also it will be helpful for understanding the code for other developers who will work on this code in future. So we are reading the data from the file path and then we are returning the dataframe.
        
        except Exception as e:
            raise SensorException(e,sys)
    

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report ={}
            for column in base_df.columns:
                d1 = base_df[column]
                d2  = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found = True 
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,)
            return status
        
        except Exception as e:
            raise SensorException(e,sys)
   

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #Reading data from train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            #Validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"
        

            #Validate numerical columns

            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns.\n"
            
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns.\n"
            
            if len(error_message)>0:
                raise Exception(error_message)

            #Let check data drift
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact
        
        except Exception as e:
            raise SensorException(e,sys)