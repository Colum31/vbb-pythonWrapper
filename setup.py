from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='vbbpy',
    version='1.1.8',
    python_requires='>3.6',
    description='A python wrapper for the VBB REST-API by derhuerst',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url="https://github.com/Colum31/vbb-pythonWrapper",
    author='colum31',
    license="MIT",
    packages=['vbbpy'],
    install_requires=['requests', 'datetime', 'geopy'],  # external packages acting as dependencies
    scripts=['examples/vbbpy-stationId', 'examples/vbbpy-stationInformation', 'examples/vbbpy-showDepartures',
             'examples/vbbpy-addressRouting']
)
