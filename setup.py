import setuptools
from distutils.core import setup
from media_downloader import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='media-downloader',
    version=__version__,
    description=long_description.split('\n')[1],
    author='ChsHub',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChsHub/media_downloader",
    packages=['media_downloader'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3', 'Topic :: Multimedia']
)
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*