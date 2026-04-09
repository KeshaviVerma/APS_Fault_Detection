from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.exception import SensorException
from sensor.logger import logging
import sys

#For Testing the exception handling in the code.
# def test_exception():
#     try:
#         logging.info("Testing exception handling for division by zero")
#         a = 1/0
#     except Exception as e:
#         raise SensorException(e, sys) #raising the exception again so that it can be handled by the caller function.

# if __name__ == "__main__": #module will be executed only when we run this file directly not when we import this file. And only this file will be executed not the other files.  
#     try:
#         test_exception()
#     except Exception as e:
#         print(e) 





# For Sending the data from csv file to mongodb collection.
# from sensor.utils2 import dump_csv_file_to_mongodb_collection

# if __name__ == "__main__":

#     file_path = "D:/APS_Fault_Detection/aps_failure_training_set1.csv"
#     database_name = "keshavi"
#     collection_name = "sensor"

#     dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)






# Data Ingestion
# Data Validation
# Data Transformation
# Model Trainer
# Model Evaluation

# if __name__ == "__main__":
#     try:
#         logging.info("Starting APS Fault Detection Training Pipeline")

#         train_pipeline = TrainPipeline()
#         train_pipeline.run_pipeline()

#         logging.info("Training pipeline completed successfully")

#     except Exception as e:
#         raise SensorException(e, sys)
    


# Now before I was running on terminal but now I will be running on FastAPI. Then I will connect, train model and model prediction.
# Because I cannot predict on same data I need new dataframe . So I want to new  CSV file . I will convert that csv file to dataframe and do prediction on itand save that file 


#For FastAPI 
from sensor.utils.main_utils import load_object
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.configuration.mongo_db_connection import MongoDBClient  
from sensor.exception import SensorException
from sensor.pipeline import training_pipeline
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Response
import pandas as pd


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!")
    
    except Exception as e:
        return Response(f"Error occurred: {e}")

#Run on terminal python main.py and then go to http://localhost:8080/
#Click on Get and then click on Try it out and then click on Execute to run the training pipeline. You will see the response in the Response Body section. If the training is successful you will see "Training successful !!" otherwise you will see the error message.    




@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        # Read CSV file and convert to dataframe
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents), na_values="na")

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()

        model = load_object(file_path=best_model_path)

        # Align features
        expected_columns = model.preprocessor.feature_names_in_
        df = df[expected_columns]

        # Predict
        y_pred = model.predict(df)

        df['predicted_column'] = y_pred

        df['predicted_column'] = df['predicted_column'].replace(
            TargetValueMapping().reverse_mapping()
        )

        df = df.fillna("NA")  # Replace NaN so JSON can handle it

        result = df.to_dict(orient="records")

        return {"prediction": result}
    
    except Exception as e:
        raise SensorException(e, sys)


def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)

#Run on http://localhost:8080/docs



#Code to create prediction_test.csv file from aps_failure_training_set1.csv file by dropping the class column and taking only first 10 rows. This file will be used for prediction in FastAPI.  
# import pandas as pd

# df = pd.read_csv("aps_failure_training_set1.csv")
# df = df.drop("class", axis=1)
# df.head(10).to_csv("prediction_test.csv", index=False)

# print("prediction_test.csv created successfully")

