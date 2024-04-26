import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycycling",
    version="0.4.0",
    author="Zachary Bull",
    author_email="zacharyedwardbull@gmail.com",
    description=(
        "A Python package for interacting with Bluetooth Low Energy (BLE) compatible bike trainers, power meters, "
        "radars and heart rate monitors"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zacharyedwardbull/pycycling",
    packages=setuptools.find_packages(),
    install_requires=["bleak"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    package_data={"": ["data/*.dat"]},
)
