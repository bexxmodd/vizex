from setuptools import setup, find_packages

with open('README.md', 'r') as rm:
    long_description = rm.read()

with open('requirements.txt') as r:
    requirements = r.read().splitlines()

setup(
    name='vizex',
    version='1.0',
    author='Beka Modebadze',
    author_email='bexxmodd@seas.upenn.edu',
    description='Terminal program to display disk space usage graphically',
    long_description=long_description,
    long_description_content_type ='text/markdown',
    url='https://github.com/bexxmodd/vizex',
    py_modules=['cli', 'disk'],
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points='''
        [console_scripts]
        vizex=cli:cli
    '''
)