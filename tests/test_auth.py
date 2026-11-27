def test_login_get_returns_200(client):
    rv = client.get("/auth/login")
    assert rv.status_code == 200


def test_register_creates_user_and_profile(app, client):
    rv = client.post(
        "/auth/register",
        data={
            "username": "testregister",
            "email": "testregister@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
            "role": "gamer",
        },
    )
    assert rv.status_code == 302
    with app.app_context():
        from models.models import User, Profile

        user = User.query.filter_by(username="testregister").first()
        assert user is not None
        assert user.email == "testregister@example.com"
        assert user.role == "gamer"
        assert user.profile is not None
        assert user.profile.nickname == "testregister"


def _ensure_tester(app):
    from werkzeug.security import generate_password_hash

    with app.app_context():
        from models.models import User, Profile, db

        user = User.query.filter_by(email="tester@example.com").first()
        if user is None:
            user = User(
                username="tester",
                email="tester@example.com",
                password=generate_password_hash("s3cret"),
                role="gamer",
            )
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
            db.session.add(Profile(user_id=user.id, nickname="Tester"))
            db.session.commit()


def test_login_success(app, client):
    _ensure_tester(app)
    rv = client.post("/auth/login", data={"email": "tester@example.com", "password": "s3cret"})
    assert rv.status_code == 302
    # Sudah login -> /profile bisa diakses (pemilik profil)
    assert client.get("/profile").status_code == 200


def test_login_fail_gives_redirect(client):
    rv = client.post("/auth/login", data={"email": "nope@example.com", "password": "wrong"})
    assert rv.status_code == 302


def test_logout(app, client):
    _ensure_tester(app)
    client.post("/auth/login", data={"email": "tester@example.com", "password": "s3cret"})
    assert client.get("/profile").status_code == 200
    rv = client.get("/auth/logout")
    assert rv.status_code == 302
    # Setelah logout, /profile harus redirect ke login
    assert client.get("/profile").status_code == 302
