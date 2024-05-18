from setuptools import setup, find_packages

setup(
    name='pyswc',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pytest>=8.1',
        'backoff>=2.2.1',
        'httpx>=0.27.0'
    ],
    include_package_data=True,
    description='A python SDK for the fake SportsWorldCentral website',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ryandaydev/portfolio-project',
    author='Ryan Day',
    author_email='ryandaydev@gmail.com',
    license='MIT',
)
