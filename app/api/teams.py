from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.config import get_db
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.crud.team import team_crud

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team"""
    # Check if team already exists
    if team_crud.exists_by_name(db, team_data.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with name '{team_data.name}' already exists"
        )
    
    try:
        return team_crud.create(db, team_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with name '{team_data.name}' already exists"
        )


@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    skip: int = Query(0, ge=0, description="Number of teams to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of teams to return"),
    db: Session = Depends(get_db)
):
    """Get all teams with pagination"""
    return team_crud.get_all(db, skip=skip, limit=limit)


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a team by ID"""
    team = team_crud.get_by_id(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID '{team_id}' not found"
        )
    return team


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team_data: TeamUpdate, db: Session = Depends(get_db)):
    """Replace a team completely (PUT)"""
    # Check if team exists
    existing_team = team_crud.get_by_id(db, team_id)
    if not existing_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID '{team_id}' not found"
        )
    
    # If name is being changed, check if new name already exists
    if team_data.name != existing_team.name:
        if team_crud.exists_by_name(db, team_data.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Team with name '{team_data.name}' already exists"
            )
    
    try:
        updated_team = team_crud.update(db, team_id, team_data)
        if not updated_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with ID '{team_id}' not found"
            )
        return updated_team
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with name '{team_data.name}' already exists"
        )


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Delete a team by ID"""
    if not team_crud.delete(db, team_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID '{team_id}' not found"
        ) 