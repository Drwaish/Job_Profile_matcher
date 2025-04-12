from pydantic import BaseModel, Field

class Reponse(BaseModel):
    """
    Response model for the API.
    """
    profile_name: str = Field(..., description="Name of the resume")
    linkedin: str = Field(..., description="LinkedIn profile URL")
    fit_score : str= Field(..., description="Fit score for the resume")
    reason : str = Field(..., description="Reason for the fit score")