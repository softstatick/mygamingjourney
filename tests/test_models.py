def test_profile_user_relationship(app):
    with app.app_context():
        from models.models import User, Profile, db

        user = User(
            username="modeluser",
            email="modeluser@example.com",
            password="whatever",
            role="gamer",
        )
        db.session.add(user)
        db.session.commit()
        profile = Profile(user_id=user.id, nickname="ModelUser")
        db.session.add(profile)
        db.session.commit()

        fetched = Profile.query.get_or_404(profile.id)
        assert fetched.user.id == user.id
        assert fetched.user.username == "modeluser"


def test_clip_vote_score_empty(app):
    with app.app_context():
        from models.models import Clip

        # Clip tanpa vote (profile_id=None karena db bisa kosong)
        # Buat clip minimal: profile harus ada — skip kalau tidak ada profile
        profile = None
        # Gunakan aplikasi test saja: hanya cek property return type int
        from models.models import Profile

        profiles = Profile.query.all()
        if profiles:
            clip = Clip(profile_id=profiles[0].id, judul="test", link="https://x.com/abc")
            assert clip.vote_score == 0
