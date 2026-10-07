from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    event_date = Column(String, nullable=False)

    total = Column(Integer, default=0)
    successful = Column(Integer, default=0)
    failed = Column(Integer, default=0)

    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    certificates = relationship(
        "Certificate",
        back_populates="job"
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("generation_jobs.id")
    )

    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)

    status = Column(String, default="pending")

    file_path = Column(String, nullable=True)

    error_message = Column(String, nullable=True)

    job = relationship(
        "GenerationJob",
        back_populates="certificates"
    )