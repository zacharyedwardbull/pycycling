# pycycling

A Python package for interacting with Bluetooth Low Energy (BLE) compatible bike trainers, power meters, radars and
heart rate monitors.

The package uses [Bleak (Bluetooth Low Energy platform Agnostic Klient)](https://github.com/hbldh/bleak)
behind the scenes to connect and communicate with bike trainers. Bleak is cross-platform with support for Windows,
MacOS, and Linux. Please refer to the Bleak repository for more information about supported platforms.

## Disclaimer

__I take no responsibility if the use of this package breaks your turbo trainer or stationary bike. Use at your own
risk!__

The package has been tested with (tested protocols in brackets):

- a Tacx NEO trainer (ANT+ FE-C over BLE, CPS, CSCS)
- a Tacx NEO 2T trainer (ANT+ FE-C over BLE, CPS, CSCS)
- an Elite Sterzo Smart steering plate (STERZO)
- a pair of Garmin Vector 3 power meter pedals (CPS)
- a Garmin RVR315 rear view radar (RDR)
- a Magene S3+ Speed/Cadence sensor (CSCS)
- an Elite Suito-T smart trainer (CPS, CSCS, FTMS)
- an Elite Justo smart trainer (CPS, CSCS, FTMS)
- an Elite Rizer grade simulator (RIZER)

Please let me know if you have used it with another device, and I will add it to the list.

## Supported protocols

* Battery Service (BAS)
* Cycling Power Service (CPS)
* Cycling Speed and Cadence Service (CSCS)
* Elite Sterzo Steering Service (STERZO)
* Elite Rizer Steering Service (RIZER)
* FiTness Machine Service (FTMS)
* Heart Rate Service (HRS)
* Rear View Radar (RDR)
* Tacx Trainer Control (ANT+ FE-C over BLE)

## Installation

Clone this repo and then run the following command from the root directory

```
python setup.py develop
```

## Documentation

Please refer to the [documentation](https://zacharybull.com/pycycling/) and
the [examples folder](https://github.com/zacharyedwardbull/pycycling/tree/master/examples) for basic usage of the
package.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/zacharyedwardbull/pycycling. This project is
intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to
the [code of conduct](https://github.com/zacharyedwardbull/pycycling/blob/master/CODE_OF_CONDUCT.md).

In terms of contributing code, pull requests increasing the features supported in each protocol are especially welcome.
If you would like to add support for another cycling related protocol, that would also be appreciated!

## Useful documentation

* ANT+ specifications (need to sign up as ANT+ adopter to access
  these): https://www.thisisant.com/developer/resources/downloads/#documents_tab
* Bluetooth Low Energy specifications: https://www.bluetooth.com/specifications/gatt/
* Bluetooth XML specification files: https://github.com/sur5r/gatt-xml
* Tacx Trainer Control
  documentation: https://github.com/jedla22/BleTrainerControl/blob/master/How-to%20FE-C%20over%20BLE%20v1_0_0.pdf
* Reverse engineering Sterzo Smart: https://www.youtube.com/watch?v=BPVFjz5zD4g
* Reverse engineering Garmin RVR315 (
  radar): https://forums.garmin.com/developer/connect-iq/f/discussion/240452/bluetooth-profile-for-garmin-varia-rtl515#pifragment-1298=3
* Bluetooth FTMS Specifications: https://www.bluetooth.org/DocMan/handlers/DownloadDoc.ashx?doc_id=423422
* Huawei HMSCore Bluetooth LE documentation (
  FTMS): https://developer.huawei.com/consumer/en/doc/development/HMSCore-Guides/ibd-0000001051005923

## Projects using pycycling

* cycling-cadence-display: https://github.com/cboddy/cycling-cadence-display
