from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import date
import json

class ProjectLinks(BaseModel):
    github: Optional[str] = None
    live: Optional[str] = None

class SkillBase(BaseModel):
    name: str
    is_top_skill: bool

class CategoryBase(BaseModel):
    name: str

class ProjectBase(BaseModel):
    title: str
    description: str

class WorkExperienceBase(BaseModel):
    company: str
    position: str
    start_date: date
    end_date: Optional[date]
    description: Optional[str]

class LinkBase(BaseModel):
    name: str
    url: str

class Skill(SkillBase):
    id: int
    
    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class Project(ProjectBase):
    id: int
    links: Optional[Dict[str, str]]
    categories: List[Category] = []

    class Config:
        from_attributes = True
    
    @staticmethod
    def from_orm_with_json(project_orm):
        project_dict = project_orm.__dict__
        if project_orm.links:
            project_dict['links'] = json.loads(project_orm.links)
        else:
            project_dict['links'] = {}
        return Project.model_validate(project_dict)


class WorkExperience(WorkExperienceBase):
    id: int
    categories: List[Category] = []

    class Config:
        from_attributes = True

class Link(LinkBase):
    id: int

    class Config:
        from_attributes = True

class Profile(BaseModel):
    name: str
    email: EmailStr
    skills: List[Skill]
    projects: List[Project]
    work_experience: List[WorkExperience]
    links: List[Link]
    
    class Config:
        from_attributes = True

class CategoryDetail(BaseModel):
    projects: List[Project]
    work_experience: List[WorkExperience]

class SkillCreate(BaseModel):
    name: str
    is_top_skill: bool = False