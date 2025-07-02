from sqlalchemy import Column, Integer, String, JSON, DateTime, Index, event
from sqlalchemy.sql import func
from app.database.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    roles = Column(JSON, default=list)  # List of role strings
    teams = Column(JSON, default=list)  # List of team strings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Ensure email uniqueness with lowercase constraint
    __table_args__ = (
        Index('ix_users_email_lower', func.lower(email), unique=True),
    )


# Event listener to enforce lowercase email before insert/update
@event.listens_for(User.email, 'set')
def lowercase_email(target, value, oldvalue, initiator):
    if value is not None:
        return value.lower()
    return value 