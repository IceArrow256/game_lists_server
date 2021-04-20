"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="game_lists_server",
    author="IceArrow256",
    author_email="icearrow256@gmail.com",
    url="https://github.com/IceArrow256/game_lists_server",
    description="Server side for game_lists app",
    version="0.0.4",
    packages=find_packages(),
    install_requires=[
        "setuptools>=45.0",
        "falcon>=3.0.0",
        "peewee>=3.14.4",
        "python-dotenv>=0.17.0",
        "requests>=2.25.1",
        "gunicorn>=20.1.0",
    ],
    entry_points={
        "console_scripts": [
            "game_lists_server=game_lists_server.__main__:main",
        ]
    },
)