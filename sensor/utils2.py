import pandas as pd
import numpy as np
import logging
import json
from sensor.config import mongo_client

def dump_csv_file_to_mongodb_collection(file_path:str,database_name:str,collection_name:str)->None:
    try:
        df= pd.read_csv(file_path)    # read the csv file using pandas
        df.reset_index(inplace=True,drop=True) # to reset the index of the dataframe
        json_records = list(json.loads(df.T.to_json()).values())       # to convert the dataframe to json format then the values of the json format to list

        mongo_client[database_name][collection_name].insert_many(json_records)  # to insert the json records to mongodb collection

    except Exception as e:
        print(e)


