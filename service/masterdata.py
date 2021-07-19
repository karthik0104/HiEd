"""
The masterdata management (MDM) service layer to handle bulk import / update of data such as Universities,
Courses and other data through CSV / Excel files into the relational SQL database.
"""
import math
import os
import json
import pandas as pd

from config.argsparser import ArgumentsParser
from entity.university import University
from entity.course import Course
from entrypoint import db
from sqlalchemy import Boolean

# Load configuration parameters
configs = ArgumentsParser()

class MasterdataService:

    field_map_file = 'config/field_map.json'
    status = None

    '''
    Method to update the database row with the incoming data row. Contains provision for field mappers as well.
    '''
    def update_data_row(self, object, row, field_map={}):
        for key, value in row.iteritems():
            if key not in field_map:
                field_map[key] = key
            if hasattr(object, field_map[key]):
                if str(Course.__table__.c[field_map[key]].type) == 'BOOLEAN':
                    value = (0 if (value=='Yes') else 1)
                setattr(object, field_map[key], value)

        return object

    def update_university_data(self, df):
        try:
            query = db.session.query(University.id, University.name)
            universities = pd.read_sql(query.statement, query.session.bind)

            # First take care of the University data
            file_universities = pd.DataFrame({'name': df['University Name'].unique()})

            # Get the consolidated list of universities
            combined_universities = pd.merge(universities, file_universities, on='name', how='outer')

            new_universities = []
            updated_universities = []

            # Iterate over the dataset and decide whether to add a new record an existing one
            for index, row in combined_universities.iterrows():
                if row['id'] is None or math.isnan(row['id']):
                    university = University(name=row['name'])
                    new_universities.append(university)
                else:
                    university = db.session.query(University).filter_by(name=row['name']).first()
                    university = self.update_data_row(university, row)
                    updated_universities.append(university)

            db.session.add_all(new_universities)
            db.session.commit()
        except:
            db.session.rollback()

        # Return updated list of universities
        return pd.read_sql(query.statement, query.session.bind)

    def update_course_data(self, df, universities):
        try:
            f = open(self.field_map_file)
            field_map = json.load(f)['course_data']

            # Now take care of Course data
            query = db.session.query(Course)
            courses = pd.read_sql(query.statement, query.session.bind)

            df = pd.merge(df, universities, how='left', left_on='University Name', right_on='name').drop(['name'], axis=1)\
                .rename(columns={'id': 'university_id'})

            # Get the consolidated list of courses
            combined_courses = pd.merge(df, courses[['id', 'name', 'university_id']]
                                        , left_on=['university_id', 'Course'], right_on=['university_id', 'name']
                                        , how='outer').drop(['name'], axis=1).rename(columns={'id': 'course_id'})

            new_courses = []
            updated_courses = []

            # Iterate over the dataset and decide whether to add a new record an existing one
            for index, row in combined_courses.iterrows():
                if row['course_id'] is None or math.isnan(row['course_id']):
                    course = Course()
                    course = self.update_data_row(course, row, field_map)
                    new_courses.append(course)
                else:
                    course = db.session.query(Course).filter_by(name=row['Course']).first()
                    course = self.update_data_row(course, row, field_map)
                    updated_courses.append(course)

            db.session.add_all(new_courses)
            db.session.commit()

            self.status = 'Success'
        except:
            db.session.rollback()
            self.status = 'Failure'

        return self.status

    def update_masterdata(self):
        # Load the master dataset
        df = pd.read_csv(os.path.join(configs.masterdata_folder, configs.university_course_file))

        universities = self.update_university_data(df)
        self.update_course_data(df, universities)

        return {'status': self.status}