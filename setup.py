from setuptools import setup, find_packages

version = {}
with open("polymera/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="polymera",
    version=version["__version__"],
    author="Peter Vegh",
    description="Representing ambiguous sequences written with complement alphabets.",
    long_description=open("pypi-readme.rst").read(),
    license="MIT",
    url="https://github.com/Edinburgh-Genome-Foundry/Polymera",
    keywords="sequence",
    packages=find_packages(exclude="docs"),
)
