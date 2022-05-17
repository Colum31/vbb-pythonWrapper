from setuptools import setup

setup(
    name='vbbpy',
    version='1.1.5',
    python_requires='>3.6',
    description='A python wrapper for the VBB REST-API by derhuerst',
    url="https://github.com/Colum31/vbb-pythonWrapper",
    author='colum31',
    license="MIT",
    packages=['vbbpy'],  # would be the same as name
    install_requires=['requests', 'datetime', 'geopy']  # external packages acting as dependencies
)
