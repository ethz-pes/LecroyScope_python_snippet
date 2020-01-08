# Python Code Snippet for Lecroy WaveSurfer 24MXs (VXI-11 Ethernet)

This **Python**P class remote controls the **PLecroy WaveSurfer 24MXs** over ethernet:
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

**Thomas Guillod** * [GitHub Profile](https://github.com/otvam)

## License

This project is licensed under the **BSD License**, see [LICENSE.md](LICENSE.md).
