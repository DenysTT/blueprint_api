from setuptools import setup, find_packages

setup(
    name='app',
    packages=find_packages(),
    version="0.1",
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-mongoengine',
        'mongoengine',
    ])
