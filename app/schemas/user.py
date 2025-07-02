from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str
    roles: List[str] = []
    teams: List[str] = []
    
    @field_validator('email')
    @classmethod
    def normalize_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower() if v else v
    
    @field_validator('roles', 'teams')
    @classmethod
    def validate_string_lists(cls, v):
        """Ensure roles and teams are lists of non-empty strings"""
        if v is None:
            return []
        return [item.strip() for item in v if item and item.strip()]


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserUpdate(UserBase):
    """Schema for full user update (PUT)"""
    pass


class UserPartialUpdate(BaseModel):
    """Schema for partial user update (PATCH)"""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    roles: Optional[List[str]] = None
    teams: Optional[List[str]] = None
    
    @field_validator('email')
    @classmethod
    def normalize_email(cls, v):
        """Normalize email to lowercase"""
        return v.lower() if v else v
    
    @field_validator('roles', 'teams')
    @classmethod
    def validate_string_lists(cls, v):
        """Ensure roles and teams are lists of non-empty strings"""
        if v is None:
            return None
        return [item.strip() for item in v if item and item.strip()]


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 