"""
User Service
Business logic for user operations
"""
from typing import List, Optional
import logging

from app.models.user import User, UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing users"""
    
    def __init__(self):
        # In production, inject database session
        self.users_db = []  # Mock database
        self.next_id = 1
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        logger.info(f"Fetching users: skip={skip}, limit={limit}")
        return self.users_db[skip : skip + limit]
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        logger.info(f"Fetching user: {user_id}")
        for user in self.users_db:
            if user.id == user_id:
                return user
        return None
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        logger.info(f"Creating user: {user_data.email}")
        from datetime import datetime
        
        new_user = User(
            id=self.next_id,
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            created_at=datetime.now()
        )
        
        self.users_db.append(new_user)
        self.next_id += 1
        
        return new_user
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        logger.info(f"Updating user: {user_id}")
        from datetime import datetime
        
        for i, user in enumerate(self.users_db):
            if user.id == user_id:
                update_data = user_data.dict(exclude_unset=True)
                updated_user = user.copy(update=update_data)
                updated_user.updated_at = datetime.now()
                self.users_db[i] = updated_user
                return updated_user
        
        return None
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        logger.info(f"Deleting user: {user_id}")
        
        for i, user in enumerate(self.users_db):
            if user.id == user_id:
                del self.users_db[i]
                return True
        
        return False