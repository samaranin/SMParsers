from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sm_parser',
    version='0.1',
    packages=find_packages(exclude=['tests*', 'examples']),
    install_requires=required,
    license='MIT',
    description='Python package to download soil moisture data from ISMN',
    long_description=open('README.md').read(),
    url='https://github.com/samaranin/SMParsers',
    author='Mykhailo Boiko',
    author_email='samaranin2912@gmail.com'
)