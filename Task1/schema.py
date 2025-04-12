from pydantic import BaseModel, Field
from typing import List


class Resume(BaseModel):
    position : str = Field(description="Position for which he is suitable")
    technical_skill: str = Field(description="Technical skills")
    experience: str = Field(description="Experience in years")

class Responseq1a(BaseModel):
    resume_name : str
    fit_score : str 
    job_matches : List[str] 