def test_public_profile_404_for_missing(client):
    rv = client.get("/gamer/999999")
    assert rv.status_code == 404


def test_browse_returns_200(client):
    rv = client.get("/browse")
    assert rv.status_code == 200
