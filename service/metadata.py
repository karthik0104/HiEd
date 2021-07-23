"""
The metadata service layer caters to providing the metdata fields and values for all the screens.
"""
import os
import pandas as pd

from config.argsparser import ArgumentsParser

# Load configuration parameters
configs = ArgumentsParser()

class MetadataService:

    def get_metadata(self):
        # Load the master dataset
        df = pd.read_csv(os.path.join(configs.masterdata_folder, configs.university_course_file))

        universities = self.update_university_data(df)
        self.update_course_data(df, universities)

        return {'status': self.status}