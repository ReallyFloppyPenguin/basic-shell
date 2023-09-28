from setuptools import setup, find_packages
from version import version
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "basic-shell/README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = version
DESCRIPTION = "A simple python-built shell"
LONG_DESCRIPTION = "A package that allows you to use a super simple and light-weight shell compared to other shell packages"

# Setting up
setup(
    name="basic-shell",
    version=VERSION,
    author="PotatoPack (Gurvaah Singh)",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["hashlib", "shutil", "os", "typing", "subprocess", "json"],
    keywords=["python", "shell", "basic"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
)
