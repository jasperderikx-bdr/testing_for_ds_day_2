"""Module to create package."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("requirements.dev.txt") as f:
    develop_requirements = f.read().splitlines()

setuptools.setup(
    name="testing_for_data_science_day_2",
    version="0.0.1",
    author="Jasper Derikx",
    author_email="jasper.derikx@bigdatarepublic.nl",
    description="Testing for data science day 2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["###", "###.*"]),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "develop": develop_requirements,
    }
)
