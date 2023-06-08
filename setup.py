from setuptools import setup

setup(
    name='beer_lambert_rt',
    version='0.1.0',
    author='Andrew P. Barrett',
    author_email='andrew.barrett@colorado.edu',
    packages=["beer_lambert_rt"],
    install_requires=[
        'pytest',
        ],
    scripts=[
        'cli/run_beer_lambert_rt',
        ],
    license='license',
    description='A Beer-Lambert radiative transfer model for sea ice',
    long_description=open('README.md').read(),
)
