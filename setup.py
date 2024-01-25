from setuptools import setup, find_packages
from version import version

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
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "click",
        "prompt_toolkit",
        "pwinput",
        "colorama",
        "datetime",
        "asyncio",
        "importlib",
        "platform",
        "webbrowser",
        "shutil",
        "hashlib",
        "json",
        "subprocess",
        "typing",
        "pyttsx3",
    ],
    keywords=["python", "shell", "basic"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
