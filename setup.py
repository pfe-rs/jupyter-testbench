from distutils.core import setup
from setuptools import find_packages

setup(
    name='testbench',
    description='Remote code unit testing for Jupyter classrooms',
    version='0.1.1',
    author='PFE Petnica',
    author_email='ele.petnica@gmail.com',
    packages=['testbench', 'testbench.tests'],
    license='LICENSE',
    install_requires=['requests', 'typing', 'scipy', 'numpy', 'matplotlib'],
)
