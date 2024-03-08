def test_download_file(client):
    response = client.get("api/v1/download/file/2024-03-03T21-52-01.mp4")
    assert response.status_code == 308
    assert str(response.data, "utf-8") == """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to target URL: <a href="http://localhost/api/v1/download/file/2024-03-03T21-52-01.mp4/">http://localhost/api/v1/download/file/2024-03-03T21-52-01.mp4/</a>.  If not click the link."""

def test_download_file_from_folder(client):
    response = client.get("api/v1/download/file/file.txt?folder_path=another_folder")
    assert response.status_code == 308
    assert str(response.data, "utf-8") == """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to target URL: <a href="http://localhost/api/v1/download/file/file.txt/?folder_path=another_folder">http://localhost/api/v1/download/file/file.txt/?folder_path=another_folder</a>.  If not click the link."""

def test_download_undefined_file(client):
    response = client.get("api/v1/download/file/dniauwduaw.dwa/")
    assert response.status_code == 404
