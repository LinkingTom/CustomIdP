from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPartialUpdate


class UserCRUD:
    def create(self, db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Email is already normalized by Pydantic validator
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            roles=user_data.roles,
            teams=user_data.teams
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email (case-insensitive)"""
        return db.query(User).filter(func.lower(User.email) == email.lower()).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    def update(self, db: Session, email: str, user_data: UserUpdate) -> Optional[User]:
        """Update user completely (PUT)"""
        db_user = self.get_by_email(db, email)
        if not db_user:
            return None
        
        # Update all fields
        db_user.email = user_data.email
        db_user.name = user_data.name
        db_user.roles = user_data.roles
        db_user.teams = user_data.teams
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def partial_update(self, db: Session, email: str, user_data: UserPartialUpdate) -> Optional[User]:
        """Update user partially (PATCH)"""
        db_user = self.get_by_email(db, email)
        if not db_user:
            return None
        
        # Update only provided fields
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def delete(self, db: Session, email: str) -> bool:
        """Delete user by email"""
        db_user = self.get_by_email(db, email)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    
    def exists(self, db: Session, email: str) -> bool:
        """Check if user exists by email"""
        return db.query(User).filter(func.lower(User.email) == email.lower()).first() is not None


# Create a singleton instance
user_crud = UserCRUD() 