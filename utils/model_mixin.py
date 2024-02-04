from app import db


class ModelMixin:
    @classmethod
    def add(cls, data):
        expected_keys = [column.name for column in cls.__table__.columns]
        filtered_data = {
            key: value for key, value in data.items() if key in expected_keys
        }
        record = cls(**filtered_data)
        db.session.add(record)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
