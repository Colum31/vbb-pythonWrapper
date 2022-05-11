from setuptools import setup

setup(
    name='vbbpy',
    version='1.1.5',
    description='A python wrapper for the VBB REST-API',
    author='Colum31',
    packages=['vbbpy'],  # would be the same as name
    install_requires=['requests', 'datetime', 'geopy']  # external packages acting as dependencies
)
