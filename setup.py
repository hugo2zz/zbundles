from setuptools import setup, find_packages

setup(
    name='zbundles',
    version="0.0.1",
    description='Data bundle for zipline.',
    packages=find_packages(include=['zbundles', 'zbundles.*']),
    install_requires=[
        'numpy',
        'pandas',
        'pycookiecheat',
        'requests',
    ],
)
