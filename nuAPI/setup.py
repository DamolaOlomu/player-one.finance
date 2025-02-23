from setuptools import setup, find_packages

setup(
    name="nuAPI",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "uvicorn",
        # other dependencies
    ],
    extras_require={
        'dev': [
            'pytest',
            # other development dependencies
        ],
    },
)

