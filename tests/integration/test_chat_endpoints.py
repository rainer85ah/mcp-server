
def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API up!"}


def test_health(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_tools(test_client):
    response = test_client.get("/api/v1/chat")
    assert response.status_code == 200
    json = response.json()
    assert "status" in json
    assert isinstance(json["status"], str)
