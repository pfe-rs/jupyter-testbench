from distutils.core import setup

setup(
    name='testbench',
    description='Remote code unit testing for Jupyter classrooms',
    version='0.1.0',
    author='PFE Petnica',
    author_email='ele.petnica@gmail.com',
    packages=['testbench', 'testbench.tests'],
    license='LICENSE',
    install_requires=['requests', 'typing'],
)
