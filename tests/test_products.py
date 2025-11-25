def test_create_product_success(authenticated_client):
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "category": "Electronics"
    }
    response = authenticated_client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 99.99
    assert response.json()["category"] == "Electronics"

def test_create_product_unauthorized(client):
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "category": "Electronics"
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 401

def test_create_product_negative_price(authenticated_client):
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": -10.00,
        "category": "Electronics"
    }
    response = authenticated_client.post("/products/", json=product_data)
    assert response.status_code == 422

def test_get_products_list(authenticated_client):
    product_data = {
        "name": "Product 1",
        "description": "First product",
        "price": 50.00,
        "category": "Books"
    }
    authenticated_client.post("/products/", json=product_data)

    response = authenticated_client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_products_pagination(authenticated_client):
    for i in range(5):
        product_data = {
            "name": f"Product {i}",
            "description": f"Product number {i}",
            "price": 10.00 + i,
            "category": "Test"
        }
        authenticated_client.post("/products/", json=product_data)

    response = authenticated_client.get("/products/?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_product_by_id(authenticated_client):
    product_data = {
        "name": "Specific Product",
        "description": "A specific product",
        "price": 75.00,
        "category": "Clothing"
    }
    create_response = authenticated_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = authenticated_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Specific Product"

def test_get_product_not_found(authenticated_client):
    response = authenticated_client.get("/products/99999")
    assert response.status_code == 404
    assert "Product not found" in response.json()["detail"]

def test_update_product_full(authenticated_client):
    product_data = {
        "name": "Original Product",
        "description": "Original description",
        "price": 100.00,
        "category": "Original"
    }
    create_response = authenticated_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    update_data = {
        "name": "Updated Product",
        "description": "Updated description",
        "price": 150.00,
        "category": "Updated"
    }
    response = authenticated_client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["price"] == 150.00

def test_patch_product_partial(authenticated_client):
    product_data = {
        "name": "Product to Patch",
        "description": "Original description",
        "price": 200.00,
        "category": "Original"
    }
    create_response = authenticated_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    patch_data = {
        "price": 250.00
    }
    response = authenticated_client.patch(f"/products/{product_id}", json=patch_data)
    assert response.status_code == 200
    assert response.json()["price"] == 250.00
    assert response.json()["name"] == "Product to Patch"

def test_delete_product(authenticated_client):
    product_data = {
        "name": "Product to Delete",
        "description": "Will be deleted",
        "price": 50.00,
        "category": "Temporary"
    }
    create_response = authenticated_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = authenticated_client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    get_response = authenticated_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_product_operations_without_token(client):
    response = client.get("/products/")
    assert response.status_code == 401

    response = client.get("/products/1")
    assert response.status_code == 401

    product_data = {
        "name": "Test",
        "price": 10.00,
        "category": "Test"
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 401

    response = client.put("/products/1", json=product_data)
    assert response.status_code == 401

    response = client.patch("/products/1", json={"price": 20.00})
    assert response.status_code == 401

    response = client.delete("/products/1")
    assert response.status_code == 401
