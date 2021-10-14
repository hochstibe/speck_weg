# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: setup.py
# Install the package

from setuptools import find_packages, setup
from pathlib import Path

readme = Path.cwd()
readme = readme.parent / 'README.md'
with open(readme, "r") as fh:
    long_description = fh.read()

setup(
    name='speck_weg_backend',
    version='0.1.0',
    author='Stefan Hochuli',
    description='Track your training progress',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'psycopg2-binary', 'environs', 'sqlalchemy', 'flask',
        'flask-sqlalchemy', 'flask-marshmallow', 'marshmallow-sqlalchemy',
        'flask-cors', 'flask-jwt-extended',
        'passlib', 'argon2-cffi', 'marshmallow'
    ],
    python_requires='>=3.9',
    url='https://github.com/hochstibe/speck_weg',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
