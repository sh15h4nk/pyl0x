from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name="pylox",
    version="0.1.0",
    author="Shiva Shankar(sh15h4nk)",
    author_email="shiva.shvvs@gmail.com",
    description="Interpreter for Lox language",
    packages= find_packages(
        where="src",
        include=["pylox", "pylox.*"]
    ),
    package_dir={"":"src"},
    entry_points={
        "console_scripts": ["pylox=pylox.lox:main"]
    }
)