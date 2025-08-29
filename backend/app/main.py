from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import json

from . import models, schemas
from .database import SessionLocal, engine



app = FastAPI(title="ME-api")

def getDataBase():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health", status_code=200)
def healthCheck():
    return {"status": "ok"}

@app.get("/profile",response_model=schemas.Profile)
def readProfile(db: Session = Depends(getDataBase)):

    profile = db.query(models.Profile).filter(models.Profile.id == 1).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    skills = db.query(models.Skill).all()
    links = db.query(models.Link).all()
    work_experience = db.query(models.WorkExperience).options(joinedload(models.WorkExperience.categories)).order_by(models.WorkExperience.start_date.desc()).all()
    projects_orm = db.query(models.Project).options(joinedload(models.Project.categories)).all()
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]

    return {
        "name": profile.name,
        "email": profile.email,
        "skills": skills,
        "projects": projects,
        "work_experience": work_experience,
        "links": links   
    }

@app.get("/skills/top", response_model=List[schemas.Skill])
def get_TopSkills(db : Session = Depends(getDataBase)):
    
    top_skills = db.query(models.Skill).filter(models.Skill.is_top_skill == True).all()
    return top_skills

@app.get("/projects", response_model=List[schemas.Project])
def get_project_by_Skill(skill: Optional[str] = None, db: Session = Depends(getDataBase)):
    query = db.query(models.Project).options(joinedload(models.Project.categories))
    
    if skill:
        query = query.join(models.project_categories).join(models.Category).filter(models.Category.name.ilike(f"%{skill}%"))
    
    projects_orm = query.all()
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]
    return projects

app.get("/search")
def search_Content(q: str, db: Session = Depends(getDataBase)):
    if not q:
        return {"projects": [], "skills": []}

    projects_orm = db.query(models.Project).options(joinedload(models.Project.categories)).filter(
        models.Project.title.ilike(f"%{q}%") | models.Project.description.ilike(f"%{q}%")
    ).all()
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]
    
    skills = db.query(models.Skill).filter(models.Skill.name.ilike(f"%{q}%")).all()
    
    return {"projects": projects, "skills": skills}

@app.get("/by-category/{category_name}", response_model=schemas.CategoryDetail)
def get_by_category(category_name: str, db: Session = Depends(getDataBase)):

    projects_orm = db.query(models.Project) \
        .options(joinedload(models.Project.categories)) \
        .join(models.project_categories) \
        .join(models.Category) \
        .filter(models.Category.name.ilike(f"%{category_name}%")) \
        .all()
    
    projects = [schemas.Project.from_orm_with_json(p) for p in projects_orm]

    work_experience = db.query(models.WorkExperience) \
        .options(joinedload(models.WorkExperience.categories)) \
        .join(models.work_experience_categories) \
        .join(models.Category) \
        .filter(models.Category.name.ilike(f"%{category_name}%")) \
        .order_by(models.WorkExperience.start_date.desc()) \
        .all()

    if not projects and not work_experience:
        raise HTTPException(
            status_code=404, 
            detail=f"No projects or work experience found for category: {category_name}"
        )

    return {"projects": projects, "work_experience": work_experience}