from setuptools import setup, find_packages

with open('README.md', 'r') as rm:
    long_description = rm.read()

with open('requirements.txt') as r:
    requirements = r.read().splitlines()

setup(
    name='vizex',
    version='2.0.4',
    author='Beka Modebadze',
    author_email='bexx.modd@gmail.com',
    description='UNIX/Linux Terminal program to graphically display the disk space usage and/or directory data',
    long_description=long_description,
    long_description_content_type ='text/markdown',
    url='https://github.com/bexxmodd/vizex',
    package_dir = {'': 'main'},
    py_modules=['cli', 'disks', 'tools', 'charts', 'battery', 'cpu', 'files', 'viztree'],
    packages = find_packages(where='main'),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points='''
        [console_scripts]
        vizex=cli:disk_usage
        vizexdf=cli:dirs_files
    '''
)