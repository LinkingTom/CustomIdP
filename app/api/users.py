from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.config import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserPartialUpdate
from app.crud.user import user_crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    if user_crud.exists(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_data.email}' already exists"
        )
    
    try:
        return user_crud.create(db, user_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_data.email}' already exists"
        )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""
    return user_crud.get_all(db, skip=skip, limit=limit)


@router.get("/{email}", response_model=UserResponse)
async def get_user(email: str, db: Session = Depends(get_db)):
    """Get a user by email"""
    user = user_crud.get_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found"
        )
    return user


@router.put("/{email}", response_model=UserResponse)
async def update_user(email: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Replace a user completely (PUT)"""
    # Check if user exists
    if not user_crud.exists(db, email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found"
        )
    
    # If email is being changed, check if new email already exists
    if user_data.email.lower() != email.lower():
        if user_crud.exists(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{user_data.email}' already exists"
            )
    
    try:
        updated_user = user_crud.update(db, email, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found"
            )
        return updated_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_data.email}' already exists"
        )


@router.patch("/{email}", response_model=UserResponse)
async def partial_update_user(email: str, user_data: UserPartialUpdate, db: Session = Depends(get_db)):
    """Update specific fields of a user (PATCH)"""
    # Check if user exists
    if not user_crud.exists(db, email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found"
        )
    
    # If email is being changed, check if new email already exists
    if user_data.email and user_data.email.lower() != email.lower():
        if user_crud.exists(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{user_data.email}' already exists"
            )
    
    try:
        updated_user = user_crud.partial_update(db, email, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found"
            )
        return updated_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_data.email}' already exists"
        )


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str, db: Session = Depends(get_db)):
    """Delete a user by email"""
    if not user_crud.delete(db, email):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' not found"
        ) 