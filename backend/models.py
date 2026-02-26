from pydantic import BaseModel
from typing import List, Optional


class RoleEvaluation(BaseModel):
    role: str
    score: int
    matched_skills: List[str]
    missing_skills: List[str]
    improvement_steps: List[str]


class EvaluationResponse(BaseModel):
    roles: List[RoleEvaluation]
    best_fit: Optional[str]
    summary: str
    
class ResourceExhaustedI(Exception):
    pass