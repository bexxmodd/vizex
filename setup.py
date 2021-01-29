from setuptools import setup, find_packages

with open('README.md', 'r') as rm:
    long_description = rm.read()

with open('requirements.txt') as r:
    requirements = r.read().splitlines()

setup(
    name='vizex',
    version='1.5.2',
    author='Beka Modebadze',
    author_email='bexxmodd@seas.upenn.edu',
    description='UNIX/Linux Terminal program to graphically display the disk space usage',
    long_description=long_description,
    long_description_content_type ='text/markdown',
    url='https://github.com/bexxmodd/vizex',
    package_dir={'': 'src'},
    py_modules=['cli', 'disks', 'tools', 'charts', 'battery', 'cpu'],
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points='''
        [console_scripts]
        vizex=cli:cli
    '''
)