"""
The metadata service layer caters to providing the metdata fields and values for all the screens.
"""
import os
import pandas as pd

from config.argsparser import ArgumentsParser
from entity.locale import LocaleField
from entrypoint import db

# Load configuration parameters
configs = ArgumentsParser()

class MetadataService:

    def get_metadata(self, current_user):
        fields_map = {}

        locale_fields = db.session.query(LocaleField).filter_by(locale_id=1).all()

        for locale_field in locale_fields:
            fields_map[locale_field.screen_name + '_' + locale_field.field_name] = locale_field.value

        return {'metadata': fields_map}