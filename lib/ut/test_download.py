def test_download_file(client):
    response = client.get("api/v1/download/file/2024-03-03T21-52-01.mp4")
    assert response.status_code == 308
    print(response.data)
    assert str(response.data, "utf-8") == """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to target URL: <a href="http://localhost/api/v1/download/file/2024-03-03T21-52-01.mp4/">http://localhost/api/v1/download/file/2024-03-03T21-52-01.mp4/</a>.  If not click the link."""
