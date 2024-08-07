from setuptools import setup, find_packages

setup(
    name="github-gitea-mirror",
    version="1.4.0",
    description="This is a demo python package that provides a data processing  via spider",
    author="chengzi",
    author_email="cz619252615@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["github-gitea-mirror=src.app:main"]},
    python_requires=">=3.6",
)
