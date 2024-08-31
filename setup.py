import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="reqrep",
    version= '2024.8.31',
    author="Erik Frojdh",
    author_email="erik.frojdh@psi.ch",
    description="Simple remote procedure call using ZMQ REQ/REP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/slsdetectorgroup/reqrep",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
