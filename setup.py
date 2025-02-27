from setuptools import setup, find_packages

setup(
    name="snakesss",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "snakesss=cli.main:app",
        ],
    },
)
