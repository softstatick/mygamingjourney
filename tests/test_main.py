def test_home_returns_200(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"MYGAMINGJOURNEY" in rv.data or b"MyGamingJourney" in rv.data


def test_about_returns_200(client):
    rv = client.get("/about")
    assert rv.status_code == 200


def test_contact_returns_200(client):
    rv = client.get("/contact")
    assert rv.status_code == 200
