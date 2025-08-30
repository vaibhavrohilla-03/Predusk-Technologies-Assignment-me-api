# Me-API Playground

This project is a personal API and portfolio playground, created as part of PreDusk Technology Pvt Ltd internship assignment. It stores my professional profile information (skills, projects, work experience, etc.) in a database and exposes it through a RESTful API. This API is consumed by a minimal, responsive frontend to display the data

## Live URLs

- **Frontend Showcase**: https://vaibhav-basic-portfolio.onrender.com
- **Live Backend API**: https://predusk-technologies-assignment-vaibhav.onrender.com
- **API Health Check**: https://predusk-technologies-assignment-vaibhav.onrender.com/health

## Tech Stack

- **Backend**: Python 3.10, FastAPI, SQLAlchemy
- **Database**: SQLite
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Deployment**: Docker, Render (Web Service for Backend, Static Site for Frontend)
- **Dev Tools**: uv for package management.

## Setup and Installation

Instructions for setting up and running the project both locally and in a production-like environment.

### Local Development Setup

**Prerequisites:**
- Git
- Python 3.10 or higher
- A virtual environment tool (e.g., venv)

**Instructions:**

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. **Setup the Backend:**

   - Create and activate a Python virtual environment:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
     ```

   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

   - Create a `.env` file in the project root for admin credentials. You can copy the example:
     Then, edit the `.env` file with a secure username and password.

   - Initialize and seed the SQLite database. This command will create `portfolio.db` in the `/data` directory and populate it with initial data.
     ```bash
     python -m backend.app.seed
     ```

   - Run the FastAPI server:
     ```bash
     uvicorn backend.app.main:app --host 127.0.0.1 --reload
     ```

   The backend API will now be running at http://127.0.0.1:8000.

3. **Setup the Frontend:**

   - Open a new terminal window.
   - Navigate to the frontend directory:
     ```bash
     cd frontend
     ```
   - Start a simple Python web server:
     ```bash
     python -m http.server 8080
     ```
   - Open your browser and go to http://127.0.0.1:8080 to view the application.

### Production Deployment

The application is deployed on Render.

- **Backend**: Deployed as a "Web Service" running a Docker container built from the provided Dockerfile. Environment variables for `ADMIN_USERNAME` and `ADMIN_PASSWORD` were configured in the Render dashboard. The service automatically redeploys on pushes to the main branch.

- **Frontend**: Deployed as a "Static Site". The configuration points to the `/frontend` directory as the publish directory. There is no build step.

## Database Schema

The schema is defined in `backend/app/schema.sql` and uses SQLite. It features tables for the profile, skills, projects, work experience, education, and uses junction tables for many-to-many relationships.

<details>
<summary>Click to view the full SQL schema</summary>

```sql
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

CREATE TABLE m_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    is_top_skill BOOLEAN DEFAULT 0
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    links TEXT
);

CREATE TABLE work_experience (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   company TEXT NOT NULL,
   position TEXT NOT NULL,
   start_date DATE NOT NULL,
   end_date DATE,
   description TEXT
);

CREATE TABLE education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT
);

CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT NOT NULL
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE project_skills (
    project_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, skill_id),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE
);

CREATE TABLE project_categories (
    project_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, category_id),
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);

CREATE TABLE work_experience_categories (
    work_experience_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (work_experience_id, category_id),
    FOREIGN KEY (work_experience_id) REFERENCES work_experience (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
```

</details>

## API Endpoints and Usage

### Sample curl Requests

Here are a few examples of how to interact with the live API.

- **Get the complete profile:**
  ```bash
  curl -X GET https://predusk-technologies-assignment-vaibhav.onrender.com/profile
  ```

- **Search for projects related to "Python":**
  ```bash
  curl -X GET "https://predusk-technologies-assignment-vaibhav.onrender.com/projects?q=python"
  ```

- **Search for projects related to "C++" (note the URL encoding for the + characters):**
  ```bash
  curl -X GET "https://predusk-technologies-assignment-vaibhav.onrender.com/projects?q=c%2B%2B"
  ```

- **Get a list of top skills:**
  ```bash
  curl -X GET https://predusk-technologies-assignment-vaibhav.onrender.com/skills/top
  ```

### Endpoint Reference

- **GET /health**: Returns a 200 OK status to indicate the API is live and running.
- **GET /profile**: Retrieves the main profile object, containing aggregated data for education, skills, projects, work experience, and links.
- **GET /projects**: Fetches a list of projects. Can be filtered with a query parameter `?q=...` which searches across both skill and category names. Supports pagination with `?skip=...` and `?limit=...`.
- **GET /skills/top**: Returns a list of all skills that are marked as a "top skill".
- **GET /search**: A broad search endpoint that looks for a query `?q=...` across project titles, descriptions, and skill names.
- **GET /by-category/{category_name}**: Retrieves all projects and work experiences associated with a specific category name.
- **POST /skills**: Creates a new skill in the database. This is a protected endpoint and requires Basic Authentication.

## Known Limitations

- **Database**: The project uses SQLite, which is file-based and not suitable for high-concurrency production applications. For a larger-scale app, a database like PostgreSQL or MySQL would be a better choice.
- **Search Functionality**: The search is performed using simple ILIKE queries, which is not as robust or efficient as a dedicated full-text search.
- **Error Handling**: The API has basic error handling but could be improved with more granular error responses and logging.

## Resume Link
 ```bash
  https://drive.google.com/file/d/1qAhRee1TLhKKiCQJmf0Tv1-mp4R8jLH7/view?usp=sharing
  ```
