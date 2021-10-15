# speck_weg
# Stefan Hochuli, 05.10.2021,
# Folder: server/tests File: conftest.py
#

import os

import pytest

from speck_weg_backend import create_app


@pytest.fixture
def app():

    app = create_app(env='testing')

    yield app
