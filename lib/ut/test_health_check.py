def test_undefined_camera_id(client):
    response = client.get("api/v1/health_check/undefined")
    assert response.status_code == 404
