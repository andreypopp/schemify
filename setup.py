from setuptools import setup, find_packages
import sys, os

version = '0.1'
install_requires = []

setup(
    name='schemify',
    version=version,
    description='Simple schema validation library',
    author='Andrey Popp',
    author_email='8mayday@gmail.com',
    py_modules=['schemify'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite='test_schemify',
    )
