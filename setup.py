from setuptools import setup
import turengcli.__main__ as m

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as file:
    requires = [line.strip() for line in file.readlines()]

VERSION = m.__version__
DESCRIPTION = "Command-line tool for tureng (tureng.com) with rich output."

setup(
    name="turengcli",
    version=VERSION,
    url="https://github.com/agmmnn/turengcli",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="agmmnn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    packages=["turengcli"],
    install_requires=requires,
    include_package_data=True,
    package_data={"turengcli": ["turengcli/*"]},
    python_requires=">=3.7",
    entry_points={"console_scripts": ["tureng = turengcli.__main__:cli"]},
)
