from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    startYear: Optional[str] = None
    endYear: Optional[str] = None

class MilitaryService(BaseModel):
    role: Optional[str] = None
    unit: Optional[str] = None
    startYear: Optional[str] = None
    endYear: Optional[str] = None

class Experience(BaseModel):
    title: Optional[str] = None
    workplace: Optional[str] = None
    startYear: Optional[str] = None
    startMonth: Optional[str] = None
    endYear: Optional[str] = None
    endMonth: Optional[str] = None
    description: Optional[str] = None

class Language(BaseModel):
    lang: Optional[str] = None
    level: Optional[str] = None

class Resume(BaseModel):
    user_id: Optional[str]
    resume_number: Optional[int]
    name: str
    email: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None
    education: Optional[List[Education]] = None
    militaryService: Optional[MilitaryService] = None
    skills: Optional[List[str]] = None
    experiences: Optional[List[Experience]] = None
    languages: Optional[List[Language]] = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "0",
                "resume_number": 1,
                "name": "bar",
                "email": "bar@example.com",
                "linkedin": "bar",
                "github": "bar",
                "summary": "bar",
                "education": [
                    {
                        "degree": "bar",
                        "institution": "string",
                        "startYear": "string",
                        "endYear": "string"
                    }
                ],
                "militaryService": {
                    "role": "string",
                    "unit": "string",
                    "startYear": "string",
                    "endYear": "string"
                },
                "skills": ["string"],
                "experiences": [
                    {
                        "title": "string",
                        "workplace": "string",
                        "startYear": "string",
                        "startMonth": "string",
                        "endYear": "string",
                        "endMonth": "string",
                        "description": "string"
                    }
                ],
                "languages": [
                    {
                        "lang": "string",
                        "level": "string"
                    }
                ]
            }
        }
