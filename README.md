# pycycling

A Python package for interacting with Bluetooth Low Energy (BLE) compatible bike trainers and power meters. 

The package uses [Bleak (Bluetooth Low Energy platform Agnostic Klient)](https://github.com/hbldh/bleak)
behind the scenes to connect and communicate with bike trainers. 
Bleak is cross-platform with support for Windows, MacOS, and Linux. 
Therefore this module should also work on these operating systems. 
Please refer to the Bleak repository for more information about supported platforms.

## Disclaimer
__I take no responsibility if the use of this package breaks your turbo trainer or stationary bike. 
Use at your own risk! 
It has only been tested with a Tacx NEO 2T trainer, and Garmin Vector 3 power meter pedals.__ 

## Supported protocols

Protocol name | Fully supported | Partially supported | Not supported
--- | --- | --- | ---
Cycling Speed and Cadence Service (CSCS) | | ✓ |
Cycling Power Service (CPS) | | ✓ |
Tacx Trainer Control (ANT+ FE-C over BLE) | | ✓ |
Elite Sterzo Steering Service | | ✓ |
FiTness Machine Service (FTMS) | | |✓

## Installation
Clone this repo and then run the following command from the root directory
```
python setup.py develop
```
## Usage
Please refer to the [examples folder](https://github.com/zacharyedwardbull/pycycling/tree/master/examples) for basic usage of the package

## Useful documentation
* ANT+ specifications (need to sign up as ANT+ adopter to access these): https://www.thisisant.com/developer/resources/downloads/#documents_tab
* Bluetooth Low Energy specifications: https://www.bluetooth.com/specifications/gatt/
* Bluetooth XML specification files: https://github.com/sur5r/gatt-xml
* Tacx Trainer Control documentation: https://github.com/jedla22/BleTrainerControl/blob/master/How-to%20FE-C%20over%20BLE%20v1_0_0.pdf
* Reverse engineering Sterzo Smart: https://www.youtube.com/watch?v=BPVFjz5zD4g