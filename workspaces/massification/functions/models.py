import datetime
import uuid

import pytz
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

TZ = pytz.timezone("America/Sao_Paulo")
Base = declarative_base()


class Contracts(Base):
    __tablename__ = "contracts_contract"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    contract = Column(String(20), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    short_description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(tz=TZ))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(tz=TZ),
        onupdate=datetime.datetime.now(tz=TZ),
    )

    def __repr__(self):
        return "<Contracts %r>" % self.id


class Vulnerabilities(Base):
    __tablename__ = "vulnerabilities_vulnerability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(tz=TZ))
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(tz=TZ),
        onupdate=datetime.datetime.now(tz=TZ),
    )

    def __repr__(self):
        return "<Vulnerabilities %r>" % self.id


class VulnerabilitiesCount(Base):
    __tablename__ = "vulnerabilities_vulnerabilitycount"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    total = Column(Integer, unique=True, nullable=False)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts_contract.id"))
    vulnerability_id = Column(UUID(as_uuid=True), ForeignKey("vulnerabilities_vulnerability.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())

    def __repr__(self):
        return "<VulnerabilitiesCount %r>" % self.id
