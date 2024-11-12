import datetime

from loguru import logger

from app import db


class ModelMixin:
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    def meta(self):
        return {
            "created_at": self.created_at,
            "created_by": self.created_by,
            "updated_at": self.updated_at,
            "updated_by": self.updated_by,
        }

    @classmethod
    def get_expected_keys(cls):
        return [c.name for c in cls.__table__.columns]

    @classmethod
    def add(cls, data: dict):
        expected_keys = cls.get_expected_keys()
        filtered_data = {k: v for k, v in data.items() if k in expected_keys}
        logger.debug(f"{filtered_data = }")
        record = cls(**filtered_data)
        logger.debug(f"{record = }")
        db.session.add(record)
        db.session.commit()
        return record

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        expected_keys = self.get_expected_keys()
        for key, value in data.items():
            if key in expected_keys:
                setattr(self, key, value)
        # setattr(self, "updated_at", datetime.datetime.utcnow())
        db.session.commit()
