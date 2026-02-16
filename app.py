from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from datetime import datetime


app = FastAPI()

class Project(BaseModel):
    id: int
    name: str
    created_at: str
    eng_name: str
    description: str
    engineer: str
    status: str
    
    @field_validator('name', 'eng_name', 'description', 'engineer')
    @classmethod
    def check_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v

class ProjectCreate(BaseModel):
    eng_name: str
    description: str
    engineer: str = "Unassigned"
    
    @field_validator('eng_name', 'description')
    @classmethod
    def check_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v

projects = []

project_id_counter = 1


@app.post("/projects")
def create_project(project_data: ProjectCreate):
    global project_id_counter
    
    for project in projects:
        if project["eng_name"] == project_data.eng_name:
            return JSONResponse(
                content={"error": "Name taken"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    new_project = {
        "id": project_id_counter,
        "name": project_data.eng_name,  
        "created_at": datetime.now().isoformat(),
        "eng_name": project_data.eng_name,
        "description": project_data.description,
        "engineer": project_data.engineer,
        "status": "in-progress"  
    }
    
    projects.append(new_project)
    project_id_counter += 1
    
    return JSONResponse(
        content=new_project,
        status_code=status.HTTP_201_CREATED
    )


@app.get("/projects")
def get_all_projects():
    return projects


@app.get("/projects/{project_id}")
def get_project_by_id(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            return project
    
    return JSONResponse(
        content={"error": "doesnt exist"},
        status_code=status.HTTP_404_NOT_FOUND
    )


@app.get("/projects/search/by-date")
def get_projects_by_date(start_date: str, end_date: str):

    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        filtered_projects = []
        for project in projects:
            project_date = datetime.fromisoformat(project["created_at"])
            if start <= project_date <= end:
                filtered_projects.append(project)
        
        if not filtered_projects:
            return JSONResponse(
                content={"error": "doesnt exist"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return filtered_projects
    
    except ValueError:
        return JSONResponse(
            content={"error": "Invalid date format. Use ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
