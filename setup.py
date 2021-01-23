import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycycling",
    version="0.0.3",
    author="Zachary Bull",
    author_email="zacharyedwardbull@gmail.com",
    description="A Python package for interacting with Bluetooth Low Energy (BLE) compatible bike trainers and power meters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zacharyedwardbull/pycycling",
    packages=setuptools.find_packages(),
    install_requires=['bleak'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={'': ['data/*.dat']},
)
