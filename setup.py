from setuptools import setup, find_packages

with open("requirement.txt") as f:
    require = f.read().splitlines()
    
    
setup(
    name="hybrid-anime-recommender",
    version="0.1",
    author="Rounak Kumar",
    packages=find_packages(),
    install_requires = require,
    
)