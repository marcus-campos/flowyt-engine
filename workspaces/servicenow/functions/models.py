import datetime
import uuid

import pytz
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

TZ = pytz.timezone("America/Sao_Paulo")
Base = declarative_base()


class WorkerFrequency(Base):
    __tablename__ = "core_workerfrequency"

    worker_name = Column(String(20), unique=True, nullable=False, primary_key=True)
    last_run_at = Column(DateTime(timezone=True), nullable=False, default=func.now())

    def __repr__(self):
        return "<WorkerFrequency %r>" % self.worker_name
