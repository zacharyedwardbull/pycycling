import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycycling", # Replace with your own username
    version="0.0.1",
    author="Zachary Bull",
    author_email="zacharyedwardbull@gmail.com",
    description="Python package for interfacing with Bluetooth Low Energy compatible bike trainers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zacharyedwardbull/pycycling",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)