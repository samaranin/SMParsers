from setuptools import setup, find_packages

setup(
    name='sm_parser',
    version='0.1',
    packages=find_packages(exclude=['tests*', 'examples']),
    license='MIT',
    description='Python package to download soil moisture data from ISMN',
    long_description=open('README.md').read(),
    url='https://github.com/samaranin/SMParsers',
    author='Mykhailo Boiko',
    author_email='samaranin2912@gmail.com'
)
