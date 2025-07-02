from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_emails: List[EmailStr] = []
    
    @field_validator('user_emails')
    @classmethod
    def normalize_emails(cls, v):
        """Normalize all emails to lowercase"""
        if v is None:
            return []
        return [email.lower() for email in v if email]


class TeamCreate(TeamBase):
    """Schema for creating a new team"""
    pass


class TeamUpdate(TeamBase):
    """Schema for full team update (PUT)"""
    pass


class TeamResponse(TeamBase):
    """Schema for team response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 