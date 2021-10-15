# speck_weg
# Stefan Hochuli, 08.10.2021,
# Folder: server/tests File: test_app.py
#

from speck_weg_backend import create_app


def test_app_factory():
    # test app
    app = create_app(env='testing')
    assert app.config['TESTING']
    # dev app
    app = create_app()
    assert not app.config['TESTING']
    assert app.config['DEBUG']
