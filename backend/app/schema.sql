DROP TABLE IF EXISTS m_profile;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS work_experience;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS education;
DROP TABLE IF EXISTS project_categories;
DROP TABLE IF EXISTS work_experience_categories;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS project_skills;

create table m_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

create table skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_top_skill BOOLEAN DEFAULT 0
);

create table projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    links TEXT
);

create table work_experience(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   company TEXT NOT NULL,
   position TEXT NOT NULL,
   start_date DATE NOT NULL,
   end_date DATE,
   description TEXT 
);

create table links(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL
);

create table categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

create table education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT
);

create table project_categories(
    project_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, category_id),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);

create table work_experience_categories(
    work_experience_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (work_experience_id, category_id),
    FOREIGN KEY (work_experience_id) REFERENCES work_experience (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);

create table project_skills (
    project_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE
);