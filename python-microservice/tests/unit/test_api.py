"""
Integration Tests for API Endpoints
"""
import pytest


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_liveness_probe(self, client):
        """Test liveness endpoint"""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
        assert "timestamp" in data
    
    def test_readiness_probe(self, client):
        """Test readiness endpoint"""
        response = client.get("/health/ready")
        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data
        assert "checks" in data


class TestUserEndpoints:
    """Test user API endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
    
    def test_create_user(self, client, sample_user_data):
        """Test creating a user"""
        response = client.post("/api/v1/users", json=sample_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]
        assert "id" in data
    
    def test_get_users(self, client):
        """Test getting all users"""
        response = client.get("/api/v1/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_and_get_user(self, client, sample_user_data):
        """Test creating and retrieving a user"""
        # Create user
        create_response = client.post("/api/v1/users", json=sample_user_data)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]
        
        # Get user
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == user_id
        assert data["email"] == sample_user_data["email"]
    
    def test_update_user(self, client, sample_user_data):
        """Test updating a user"""
        # Create user
        create_response = client.post("/api/v1/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Update user
        update_data = {"full_name": "Updated Name"}
        update_response = client.put(f"/api/v1/users/{user_id}", json=update_data)
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["full_name"] == "Updated Name"
    
    def test_delete_user(self, client, sample_user_data):
        """Test deleting a user"""
        # Create user
        create_response = client.post("/api/v1/users", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Delete user
        delete_response = client.delete(f"/api/v1/users/{user_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_user(self, client):
        """Test getting non-existent user"""
        response = client.get("/api/v1/users/999999")
        assert response.status_code == 404