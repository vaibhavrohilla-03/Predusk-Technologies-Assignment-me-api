from sqlalchemy import (
    Boolean, Column, Integer, String, Text, Date, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from .database import Base

project_categories = Table('project_categories', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

work_experience_categories = Table('work_experience_categories', Base.metadata,
    Column('work_experience_id', Integer, ForeignKey('work_experience.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

project_skills = Table('project_skills', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class Profile(Base):
    __tablename__ = 'm_profile'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    is_top_skill = Column(Boolean, default=False)
    
    projects = relationship('Project', secondary=project_skills, back_populates='skills')


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    links = Column(Text)
    
    categories = relationship('Category', secondary=project_categories, back_populates='projects')
    skills = relationship('Skill', secondary=project_skills, back_populates='projects')


class WorkExperience(Base):
    __tablename__ = 'work_experience'
    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Text)

    categories = relationship('Category', secondary=work_experience_categories, back_populates='work_experiences')


class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    institution = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String)


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    projects = relationship('Project', secondary=project_categories, back_populates='categories')
    work_experiences = relationship('WorkExperience', secondary=work_experience_categories, back_populates='categories')