from datetime import datetime

from loguru import logger

from wtforms import DateField
from wtforms.fields.choices import SelectField
from app import db


class FormMixin:
    def set_data_from_data(self, data: dict):
        for field_name, field_value in data.items():
            if field_name in self._fields:
                field = getattr(self, field_name)
                if isinstance(field, DateField) and isinstance(field_value, str):
                    logger.debug("Converting string field value to date ...")
                    field_value = datetime.strptime(field_value, "%Y-%m-%d").date()
                setattr(field, "data", field_value)

    def set_data_from_model(self, model: db.Model):
        for field_name, field_value in model.__dict__.items():
            if field_name in self._fields:
                field = getattr(self, field_name)
                if isinstance(field, DateField) and isinstance(field_value, str):
                    logger.debug("Converting string field value to date ...")
                    field_value = datetime.strptime(field_value, "%Y-%m-%d").date()
                # if isinstance(field, SelectField):
                #     print(type(field_value))
                #     # if isinstance(field_value, datetime.time):
                #     #     logger.error("afdafdas")
                #     #     field_value = field_value.strptime("%I:%M")
                setattr(field, "data", field_value)
