from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="contagion",
    version="1.2.1",
    author="Lucas McCabe",
    author_email="lucashmccabe@gmail.com",
    description="a Python package for node immunization and network contagion simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucasmccabe/contagion",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
