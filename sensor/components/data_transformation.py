import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline


from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.entity.artifact_entity import (DataTransformationArtifact, DataValidationArtifact)
from sensor.entity.config_entity import DataTransformationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.ml.model.estimator import TargetValueMapping
from sensor.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        """
        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise SensorException(e, sys)


    @staticmethod                             #static method can be called without creating an object of the class. It is a method that belongs to the class rather than an instance of the class. It does not have access to the instance (self) or class (cls) variables. It is defined using the @staticmethod decorator and does not take any special first argument like self or cls.
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise SensorException(e, sys)


    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            logging.info("Creating preprocessing pipeline")
            
            robust_scaler = RobustScaler()
            
            simple_imputer = SimpleImputer(strategy="mean")
            
            preprocessor = Pipeline(
                steps=[
                    ("Imputer", simple_imputer), #replace missing values with zero
                    ("RobustScaler", robust_scaler) #keep every feature in same range and handle outlier
                    ]
            )
            
            return preprocessor

        except Exception as e:
            raise SensorException(e, sys) from e

    
    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")

            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            preprocessor = self.get_data_transformer_object()


            # =============================
            # Separate input and target
            # =============================

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Mapping target values (pos → 1, neg → 0)
            target_feature_train_df = target_feature_train_df.map(TargetValueMapping().to_dict())
            target_feature_test_df = target_feature_test_df.map(TargetValueMapping().to_dict())
            
            # =============================
            # Fit preprocessing pipeline
            # =============================

            logging.info("Fitting preprocessing object")

            preprocessor_object = preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            # =============================
            # Handle class imbalance
            # =============================
            
            logging.info("Applying SMOTETomek on training data")

            smt = SMOTETomek(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(transformed_input_train_feature, target_feature_train_df)

            # Do NOT apply SMOTE on test data
            input_feature_test_final = transformed_input_test_feature
            target_feature_test_final = target_feature_test_df

            # =============================
            # Convert to numpy arrays
            # =============================

            train_arr = np.c_[
                input_feature_train_final,
                np.array(target_feature_train_final)
            ]

            test_arr = np.c_[
                input_feature_test_final,
                np.array(target_feature_test_final)
            ]

            # =============================
            # Save transformed data
            # =============================

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)

            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path,  preprocessor_object)

            # =============================
            # Create artifact
            # =============================

            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(f"Data transformation artifact created: {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys) from e