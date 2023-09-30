from setuptools import find_packages, setup

pkgs = find_packages("src")

name = pkgs[0]

setup(
    entry_points={
        "console_scripts": [
            f"{name}={name}.__main__:cli",
        ],
    },
    install_requires=[
        "TexSoup==0.3.1",
    ],
    name=name,
    packages=pkgs,
    package_dir={"": "src"},
)
