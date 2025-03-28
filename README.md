# Python Code for Lecroy WaveSurfer 24MXs (Ethernet)

![license - BSD](https://img.shields.io/badge/license-BSD-green)
![language - python](https://img.shields.io/badge/language-python-blue)
![category - power electronics](https://img.shields.io/badge/category-power%20electronics-lightgrey)
![status - unmaintained](https://img.shields.io/badge/status-unmaintained-red)

This **Python** class remote controls the **Lecroy WaveSurfer 24MXs** over ethernet:
* connect to the device
* set up the channels
* control the trigger
* download a screenshot
* download the waveform data

This class:
* uses the "VXI-11" ethernet instrument control protocol
* was tested on "MS Windows" but should run with Linux
* should also be easy to adapt to other Lecroy scopes
* was tested with Python 2.7 but should run with Python 3.x

This class is meant as a lightweight code to be used as a "code snippet" and not as a full package.
Be careful, the Lecroy instruction are messy and incoherent between the scope models.

## Author

* **Thomas Guillod, ETH Zurich, Power Electronic Systems Laboratory** - [GitHub Profile](https://github.com/otvam)

## License

* This project is licensed under the **BSD License**, see [LICENSE.md](LICENSE.md).
* This project is copyrighted by: (c) 2020, ETH Zurich, Power Electronic Systems Laboratory, T. Guillod.
