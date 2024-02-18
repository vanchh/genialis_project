from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="progeny",
    version="0.1",
    author="Anja Vrečer",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'progeny = progeny.progeny:main'
        ]
    },
    install_requires=requirements
)
