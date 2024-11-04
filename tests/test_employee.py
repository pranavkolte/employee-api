from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "server is running"}

def test_create_user():
    response = client.post("/api/user/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json()["message"] == "User testuser created successfully"

def test_create_user_existing_username():
    # Assuming "testuser" already exists from the previous test
    response = client.post("/api/user/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 403
    assert "username: testuser already exist" in response.json()["message"]

def test_create_employee():
    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]

    # Use the token to create an employee
    response = client.post(
        "/api/employee/",
        json={"name": "Test User", "email": "test.user@example.com", "department": "HR", "role": "Manager"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["message"] == "employee with test.user@example.com created"

def test_create_employee_existing_email():
    # Authenticate to get a token
    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]

    response = client.post(
        "/api/employee/",
        json={"name": "Test User", "email": "test.user@example.com", "department": "Finance", "role": "Analyst"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert "email: test.user@example.com already exist" in response.json()["message"]
