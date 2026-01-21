from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Company
from app.schemas import CompanyCreate, CompanyRead, CompanyUpdate
from app.core.dependencies import get_current_user, require_recruiter

router = APIRouter(prefix="/companies", tags=["companies"])

# Create a company, recruiter-only
@router.post("/", response_model=CompanyRead)
def create_company(company: CompanyCreate, current_user=Depends(require_recruiter), session: Session = Depends(get_session)):
    db_company = Company(
        name=company.name,
        description=company.description,
        owner_id=current_user.id
    )
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

# List all companies, public
@router.get("/", response_model=list[CompanyRead])
def list_companies(session: Session = Depends(get_session)):
    companies = session.exec(select(Company)).all()
    return companies

# Get a single company by ID,  public
@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, session: Session = Depends(get_session)):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

# Update company, recruiter-only, must own the company
@router.put("/{company_id}", response_model=CompanyRead)
def update_company(company_id: int, company_update: CompanyUpdate, current_user=Depends(require_recruiter), session: Session = Depends(get_session)):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this company")
    if company_update.name is not None:
        company.name = company_update.name
    if company_update.description is not None:
        company.description = company_update.description
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

# Delete company, recruiter-only, must own the company
@router.delete("/{company_id}")
def delete_company(company_id: int, current_user=Depends(require_recruiter), session: Session = Depends(get_session)):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if company.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this company")
    session.delete(company)
    session.commit()
    return {"detail": "Company deleted"}