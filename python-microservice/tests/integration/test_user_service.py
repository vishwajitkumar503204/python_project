"""
Unit Tests for User Service
"""
import pytest
from app.services.user_service import UserService
from app.models.user import UserCreate, UserUpdate


@pytest.mark.asyncio
class TestUserService:
    """Test suite for UserService"""
    
    @pytest.fixture
    def service(self):
        """Create UserService instance"""
        return UserService()
    
    async def test_create_user(self, service, sample_user_data):
        """Test user creation"""
        user_create = UserCreate(**sample_user_data)
        user = await service.create_user(user_create)
        
        assert user.id == 1
        assert user.email == sample_user_data["email"]
        assert user.username == sample_user_data["username"]
        assert user.created_at is not None
    
    async def test_get_user(self, service, sample_user_data):
        """Test getting user by ID"""
        # Create user first
        user_create = UserCreate(**sample_user_data)
        created_user = await service.create_user(user_create)
        
        # Get user
        user = await service.get_user(created_user.id)
        
        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email
    
    async def test_get_user_not_found(self, service):
        """Test getting non-existent user"""
        user = await service.get_user(999)
        assert user is None
    
    async def test_get_users(self, service, sample_user_data):
        """Test getting all users"""
        # Create multiple users
        for i in range(3):
            user_data = sample_user_data.copy()
            user_data["email"] = f"test{i}@example.com"
            user_data["username"] = f"testuser{i}"
            user_create = UserCreate(**user_data)
            await service.create_user(user_create)
        
        users = await service.get_users()
        assert len(users) == 3
    
    async def test_update_user(self, service, sample_user_data):
        """Test updating user"""
        # Create user
        user_create = UserCreate(**sample_user_data)
        created_user = await service.create_user(user_create)
        
        # Update user
        update_data = UserUpdate(full_name="Updated Name")
        updated_user = await service.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.full_name == "Updated Name"
        assert updated_user.updated_at is not None
    
    async def test_delete_user(self, service, sample_user_data):
        """Test deleting user"""
        # Create user
        user_create = UserCreate(**sample_user_data)
        created_user = await service.create_user(user_create)
        
        # Delete user
        result = await service.delete_user(created_user.id)
        assert result is True
        
        # Verify deletion
        user = await service.get_user(created_user.id)
        assert user is None
    
    async def test_delete_user_not_found(self, service):
        """Test deleting non-existent user"""
        result = await service.delete_user(999)
        assert result is False