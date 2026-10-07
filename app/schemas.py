from pydantic import BaseModel, EmailStr
from typing import List


class Recipient(BaseModel):
    name: str
    email: EmailStr


class CertificateJobRequest(BaseModel):
    event_name: str
    event_date: str
    recipients: List[Recipient]