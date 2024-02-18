from setuptools import setup, find_packages


setup(
    name="progeny",
    version="0.1",
    author="Anja Vrecer",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'progeny = progeny.progeny:main'
        ]
    }
)
