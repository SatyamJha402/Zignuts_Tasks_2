from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlmodel import Session, select
from app.database import get_session
from app.models import Job
from app.schemas import JobCreate, JobRead, JobUpdate
from app.core.dependencies import get_current_user, require_recruiter
from app.models import Tag
from app.models import JobTag
from sqlalchemy import func

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Create a job, recruiter-only
@router.post("/", response_model=JobRead)
def create_job(job: JobCreate = Body(...), current_user=Depends(require_recruiter), session: Session = Depends(get_session)):

    db_job = Job(
        title=job.title,
        description=job.description,
        location=job.location,
        company_id=job.company_id,
        created_by=current_user.id
    )
    session.add(db_job)
    session.commit()
    session.refresh(db_job)

    # Handle tags
    for tag_name in job.tags:
        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        #create tag if it doesn't exist
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()
            session.refresh(tag)

        link = JobTag(job_id=db_job.id, tag_id=tag.id)
        session.add(link)

    session.commit()

    return db_job
    # return JobRead(
    #     **db_job.dict(),
    #     tags=job.tags
    # )


# List jobs, public
@router.get("/")
def list_jobs(
    session: Session = Depends(get_session),
    tag: str | None = None,
    location: str | None = None,
    company_id: int | None = None,
    q: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    query = select(Job)
    if location:
        query = query.where(Job.location.ilike(f"%{location}%"))
    if company_id:
        query = query.where(Job.company_id == company_id)
    if q:
        query = query.where(Job.title.ilike(f"%{q}%"))
    if tag:
        query = (
            query
            .join(JobTag, JobTag.job_id == Job.id)
            .join(Tag, Tag.id == JobTag.tag_id)
            .where(Tag.name == tag)
        )

    # Count total
    total = session.exec(
        select(func.count()).select_from(query.subquery())
    ).one()

    # for pagination
    offset = (page - 1) * limit
    jobs = session.exec(query.offset(offset).limit(limit)).all()

    # Load tags
    results = []
    for job in jobs:
        tags = session.exec(
            select(Tag.name)
            .join(JobTag, JobTag.tag_id == Tag.id)
            .where(JobTag.job_id == job.id)
        ).all()

        results.append({
            **job.dict(),
            "tags": tags
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": results
    }


# Get single job by ID, public
@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Update job, recruiter-only, must own the job
@router.put("/{job_id}", response_model=JobRead)
def update_job(job_id: int, job_update: JobUpdate, current_user=Depends(require_recruiter), session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    #checks for job existence
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    #ownership
    if job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this job")
    #update fields
    if job_update.title is not None:
        job.title = job_update.title
    if job_update.description is not None:
        job.description = job_update.description
    if job_update.location is not None:
        job.location = job_update.location
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

# Delete job, recruiter-only, must own the job
@router.delete("/{job_id}")
def delete_job(job_id: int, current_user=Depends(require_recruiter), session: Session = Depends(get_session)):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this job")
    session.delete(job)
    session.commit()
    return {"detail": "Job deleted"}