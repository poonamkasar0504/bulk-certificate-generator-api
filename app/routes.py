from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import os

from .database import get_db
from .models import GenerationJob, Certificate
from .schemas import CertificateJobRequest
from .certificate import generate_certificate


router = APIRouter()


@router.post("/jobs")
def create_job(
    request: CertificateJobRequest,
    db: Session = Depends(get_db)
):

    job = GenerationJob(
        event_name=request.event_name,
        event_date=request.event_date,
        total=len(request.recipients),
        status="processing"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="processing"
        )

        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        try:
            file_path = generate_certificate(
                recipient.name,
                request.event_name,
                request.event_date,
                certificate.id
            )

            certificate.status = "completed"
            certificate.file_path = file_path

            job.successful += 1

        except Exception as e:

            certificate.status = "failed"
            certificate.error_message = str(e)

            job.failed += 1

        db.commit()

    job.status = "completed"

    db.commit()

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }


@router.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

    job = db.query(
        GenerationJob
    ).filter(
        GenerationJob.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }


@router.get("/certificates/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):

    certificate = db.query(
        Certificate
    ).filter(
        Certificate.id == certificate_id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Certificate is not available"
        )

    if not os.path.exists(certificate.file_path):
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )