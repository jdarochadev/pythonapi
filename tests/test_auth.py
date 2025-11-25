def test_register_user_success(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "newuser@example.com"
    assert "password" not in response.json()

def test_register_duplicate_username(client, test_user):
    user_data = {
        "username": test_user["username"],
        "email": "different@example.com",
        "password": "password123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 409
    assert "Username already exists" in response.json()["detail"]

def test_register_duplicate_email(client, test_user):
    user_data = {
        "username": "differentuser",
        "email": test_user["email"],
        "password": "password123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 409
    assert "Email already exists" in response.json()["detail"]

def test_login_success(client, test_user):
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client, test_user):
    login_data = {
        "username": test_user["username"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_refresh_token_success(client, test_user):
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    refresh_token = login_response.json()["refresh_token"]

    refresh_data = {"refresh_token": refresh_token}
    response = client.post("/auth/refresh", json=refresh_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_refresh_token_invalid(client):
    refresh_data = {"refresh_token": "invalid_token"}
    response = client.post("/auth/refresh", json=refresh_data)
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]
