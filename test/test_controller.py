from fastapi.testclient import TestClient
from unittest.mock import patch
from src.controller import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Service is working",
                               "version": "0.1.1"}


@patch('src.controller.create_image')  # mock of create image function
def test_generate_image(mock_create_image):
    mock_create_image.return_value = None
    response = client.post("/generate-image", json={"description": "test"})
    assert response.status_code == 200
    assert "task_id" in response.json()
    mock_create_image.assert_called_once()


@patch('os.path.exists')  # mock of path exist
def test_get_status(mock_exists):
    mock_exists.return_value = True  # path exist always
    task_id = "fake-id"
    response = client.get(f"/status/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "completed", "url": f"/download/{task_id}"}


def test_download_image():
    task_id = "fake-id"
    response = client.get(f"/download/{task_id}")
    assert response.status_code == 200
