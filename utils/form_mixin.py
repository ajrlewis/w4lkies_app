from datetime import datetime
from wtforms import DateField
from app import db


class FormMixin:
    def set_data_from_model(self, model: db.Model):
        for field_name, field_value in model.__dict__.items():
            if field_name in self._fields:
                field = getattr(self, field_name)
                if isinstance(field, DateField) and isinstance(field_value, str):
                    field_value = datetime.strptime(field_value, "%Y-%m-%d").date()
                setattr(field, "data", field_value)
