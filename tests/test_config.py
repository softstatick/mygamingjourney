def test_config_loads():
    from config import Config

    assert Config.SECRET_KEY == "test-secret-key"
    assert Config.DEBUG is False
    assert Config.PORT == 5000


def test_allowed_file():
    from config import allowed_file

    assert allowed_file("foto.jpg")
    assert allowed_file("poto.PNG")
    assert not allowed_file("readme.exe")
    assert not allowed_file("tanpa_ekstensi")
