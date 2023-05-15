# aditof.py

Demo python script that interfaces with the `aditofpython` library and shows the camera feeds of Analog Devices ToF Cameras.
I've only tested this with the AD-FXTOF1, but it should work with any other ADI ToF camera as well.

The actual interfacing with the camera is largely copied from the [first_frame.py](https://github.com/analogdevicesinc/aditof_sdk/blob/master/bindings/python/examples/first_frame/first_frame.py) example, which is part of the [ADI ToF SDK](https://github.com/analogdevicesinc/aditof_sdk).

This projects adds command line parameters for choosing between the different camera modes and hides the debug output behind the verbose option.
The depth and IR images are shown via opencv imshow.
The depth image is converted to the popular jet color scheme for better visualization.

```bash
$ ./aditof.py --help
usage: ./aditof_test.py [-h] [-v] [-n | -m]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Enable verbose output. This will print additional debug
                 information to stdout
  -n, --near     Configures the camera to "near" mode (default)
  -m, --medium   Configures the camera to "medium" mode

```

# Requirements

You'll need the `aditofpython` binding, the OpenCV binding for python and the python module `argparse`.
I used a [precompiled raspberry pi image](https://github.com/analogdevicesinc/aditof_sdk#supported-embedded-platforms) and pip installed opencv-python and argparse.

# License

AD's first_frame.py example is released under the BSD 3-clause license.
My own contributions are released under the same license.
For more information, see the LICENSE file.
