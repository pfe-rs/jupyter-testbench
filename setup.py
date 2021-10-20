from distutils.core import setup
from setuptools import find_packages

setup(
    name='testbench',
    description='Remote code unit testing for Jupyter classrooms',
    version='0.1.2',
    author='PFE Petnica',
    author_email='ele.petnica@gmail.com',
    packages=find_packages(exclude=['dashboard']),
    package_data={'': ['*.png']},
    license='LICENSE',
    install_requires=['requests', 'typing'],
)
