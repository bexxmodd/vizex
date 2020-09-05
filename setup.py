from setuptools import setup, find_packages

setup(
    name='vizex',
    version='0.5',
    py_modules=['cli', 'main'],
    packages = find_packages(),
    install_requires=[
        'click==7.1.2',
        'colored==1.4.2',
        'psutil==5.7.2'
    ],
    entry_points='''
        [console_scripts]
        vizex=cli:cli
    '''
)