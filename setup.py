from setuptools import setup, find_packages

setup(name="switchsimulator", packages=find_packages(
    where="src"), package_dir={"": "src"})
