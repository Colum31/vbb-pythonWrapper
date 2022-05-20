from setuptools import setup

setup(
    name='vbbpy',
    version='1.1.6',
    python_requires='>3.6',
    description='A python wrapper for the VBB REST-API by derhuerst',
    url="https://github.com/Colum31/vbb-pythonWrapper",
    author='colum31',
    license="MIT",
    packages=['vbbpy'],
    install_requires=['requests', 'datetime', 'geopy'],  # external packages acting as dependencies
    scripts=['examples/vbbpy-stationId', 'examples/vbbpy-stationInformation', 'examples/vbbpy-showDepartures',
             'examples/vbbpy-addressRouting']
)
