from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


class TeamCRUD:
    def create(self, db: Session, team_data: TeamCreate) -> Team:
        """Create a new team"""
        db_team = Team(
            name=team_data.name,
            description=team_data.description,
            user_emails=team_data.user_emails
        )
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team
    
    def get_by_name(self, db: Session, name: str) -> Optional[Team]:
        """Get team by name"""
        return db.query(Team).filter(Team.name == name).first()
    
    def get_by_id(self, db: Session, team_id: int) -> Optional[Team]:
        """Get team by ID"""
        return db.query(Team).filter(Team.id == team_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
        """Get all teams with pagination"""
        return db.query(Team).offset(skip).limit(limit).all()
    
    def update(self, db: Session, team_id: int, team_data: TeamUpdate) -> Optional[Team]:
        """Update team completely"""
        db_team = self.get_by_id(db, team_id)
        if not db_team:
            return None
        
        # Update all fields
        db_team.name = team_data.name
        db_team.description = team_data.description
        db_team.user_emails = team_data.user_emails
        
        db.commit()
        db.refresh(db_team)
        return db_team
    
    def delete(self, db: Session, team_id: int) -> bool:
        """Delete team by ID"""
        db_team = self.get_by_id(db, team_id)
        if not db_team:
            return False
        
        db.delete(db_team)
        db.commit()
        return True
    
    def exists_by_name(self, db: Session, name: str) -> bool:
        """Check if team exists by name"""
        return db.query(Team).filter(Team.name == name).first() is not None


# Create a singleton instance
team_crud = TeamCRUD() 