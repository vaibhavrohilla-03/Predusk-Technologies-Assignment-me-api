from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from . import models, schemas, dependencies
from .database import SessionLocal

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("api.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="ME-api")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

def getDataBase():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health", status_code=200, tags=["Status"])
def healthCheck():
    return {"status": "ok"}


@app.get("/profile", response_model=schemas.Profile, tags=["Profile"])
@limiter.limit("10/minute")
def readProfile(request: Request, db: Session = Depends(getDataBase)):
    profile = db.query(models.Profile).filter(models.Profile.id == 1).first()
    if not profile:
        logger.error("Profile with ID 1 not found in the database.")
        raise HTTPException(status_code=404, detail="Profile not found")

    education = db.query(models.Education).order_by(models.Education.start_date.desc()).all()
    projects_orm = db.query(models.Project).options(
        joinedload(models.Project.categories), 
        joinedload(models.Project.skills)
    ).all()
    skills = db.query(models.Skill).order_by(models.Skill.is_top_skill.desc(), models.Skill.name).all()
    links = db.query(models.Link).all()
    work_experience = db.query(models.WorkExperience).options(joinedload(models.WorkExperience.categories)).order_by(models.WorkExperience.start_date.desc()).all()
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]

    return {
        "name": profile.name,
        "email": profile.email,
        "education": education,
        "skills": skills,
        "projects": projects,
        "work_experience": work_experience,
        "links": links   
    }


@app.get("/skills/top", response_model=List[schemas.Skill], tags=["Skills"])
def get_TopSkills(db: Session = Depends(getDataBase)):
    top_skills = db.query(models.Skill).filter(models.Skill.is_top_skill == True).all()
    return top_skills


@app.post("/skills", response_model=schemas.Skill, status_code=status.HTTP_201_CREATED, tags=["Skills"])
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(getDataBase), username: str = Depends(dependencies.get_current_username)):
    db_skill = models.Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.get("/projects", response_model=List[schemas.Project], tags=["Projects"])
def get_project_by_Skill(skill: Optional[str] = None, db: Session = Depends(getDataBase), skip: int = 0, limit: int = 10):
    query = db.query(models.Project).options(
        joinedload(models.Project.categories), 
        joinedload(models.Project.skills)
    )
    if skill:
        query = query.join(models.project_skills).join(models.Skill).filter(models.Skill.name.ilike(f"%{skill}%"))
    
    projects_orm = query.order_by(models.Project.id).offset(skip).limit(limit).all()
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]
    return projects


@app.get("/search", tags=["Search"])
def search_Content(q: str, db: Session = Depends(getDataBase)):
    logger.info(f"Search performed with query '{q}'")
    if not q:
        return {"projects": [], "skills": []}

    projects_orm = db.query(models.Project).options(
        joinedload(models.Project.categories),
        joinedload(models.Project.skills) 
    ).filter(
        models.Project.title.ilike(f"%{q}%") | models.Project.description.ilike(f"%{q}%")
    ).all()
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]
    
    skills = db.query(models.Skill).filter(models.Skill.name.ilike(f"%{q}%")).all()
    
    return {"projects": projects, "skills": skills}


@app.get("/by-category/{category_name}", response_model=schemas.CategoryDetail, tags=["Categories"])
def get_by_category(category_name: str, db: Session = Depends(getDataBase)):
    projects_orm = db.query(models.Project) \
        .options(joinedload(models.Project.categories), joinedload(models.Project.skills)) \
        .join(models.project_categories).join(models.Category) \
        .filter(models.Category.name.ilike(f"%{category_name}%")) \
        .all()
    
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]

    work_experience = db.query(models.WorkExperience) \
        .options(joinedload(models.WorkExperience.categories)) \
        .join(models.work_experience_categories).join(models.Category) \
        .filter(models.Category.name.ilike(f"%{category_name}%")) \
        .order_by(models.WorkExperience.start_date.desc()) \
        .all()

    if not projects and not work_experience:
        raise HTTPException(
            status_code=404, 
            detail=f"No projects or work experience found for category: {category_name}"
        )

    return {"projects": projects, "work_experience": work_experience}