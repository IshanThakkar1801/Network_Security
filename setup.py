'''
The setup.py file is an essential part of packaging and distributing a Python project. It is used by setuptools to define the configuration of your project, such as its metadata, dependencies, and entry points. Below is an example of a setup.py file that you can use as a template for your project.'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Reads the requirements.txt file and returns a list of dependencies."""
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
            ## Proecess every line
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_lst

setup(
    name='network_security',
    version='0.0.1',
    author='Ishan Thakkar',
    author_email='ishan.1801@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)